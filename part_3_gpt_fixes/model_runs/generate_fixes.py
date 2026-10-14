"""Generate one fixed file per case/model. Never execute generated code or tests."""
import argparse
import ast
import csv
import hashlib
import importlib.util
import io
import json
import os
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


def utcnow():
    return datetime.now(timezone.utc).isoformat()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def atomic_text(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + '.tmp')
    temp.write_text(text, encoding='utf-8')
    temp.replace(path)


def write_json(path, value):
    atomic_text(path, json.dumps(value, indent=2, ensure_ascii=False) + '\n')


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))


def load_experiment(root):
    manifest = read_json(root / '_shared' / 'manifest.json')
    assert len(manifest['cases']) == 73
    assert len({c['case'] for c in manifest['cases']}) == 73
    assert sum(len(c['versions']) for c in manifest['cases']) == 1015
    assert manifest['reasoning_effort'] == 'medium'
    prompt_path = root / '_shared' / 'prompt.json'
    assert sha(prompt_path.read_bytes()) == manifest['prompt_sha256'], 'Prompt changed'
    helper_path = root / '_shared' / 'preprocessing.py'
    assert sha(helper_path.read_bytes()) == manifest['preprocessing_sha256'], 'Preprocessing changed'
    spec = importlib.util.spec_from_file_location('frozen_preprocessing', helper_path)
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    prompts = read_json(prompt_path)
    for entry in manifest['cases']:
        folder = root / '_shared' / 'inputs' / entry['case']
        for name, digest in entry['input_sha256'].items():
            assert sha((folder / name).read_bytes()) == digest, f'Input changed: {entry["case"]}/{name}'
        messages = read_json(folder / 'messages.json')
        expected = [{'role': 'system', 'content': prompts['SYSTEM']},
                    {'role': 'user', 'content': prompts['USER'].format(
                        question=(folder / 'question.txt').read_text(encoding='utf-8'),
                        code=(folder / 'buggy_stripped.py').read_text(encoding='utf-8'))}]
        assert messages == expected, f'Message mismatch: {entry["case"]}'
    return manifest, helper


def request_for(root, model, entry):
    return {'model': model, 'reasoning_effort': 'medium',
            'messages': read_json(root / '_shared' / 'inputs' / entry['case'] / 'messages.json')}


def redact_error(exc, key):
    text = f'{type(exc).__name__}: {exc}'
    if key:
        text = text.replace(key, '[REDACTED]')
    return re.sub(r'sk-[A-Za-z0-9_-]+', '[REDACTED]', text)


def finish_response(folder, entry, model, response, helper):
    choices = response.get('choices') or []
    choice = choices[0] if choices else {}
    message = choice.get('message') or {}
    raw = message.get('content') or ''
    if not isinstance(raw, str):
        raw = ''
    atomic_text(folder / 'raw_reply.txt', raw)
    state = {'case': entry['case'], 'model': model, 'reasoning_effort': 'medium',
             'completed_utc': utcnow(), 'returned_model': response.get('model'),
             'response_id': response.get('id'), 'finish_reason': choice.get('finish_reason'),
             'usage': response.get('usage'), 'fix_created': False, 'syntax_check': 'NOT CHECKED',
             'error': '', 'status': 'RESPONSE_ERROR', 'fix_file': None,
             'input_sha256': entry['input_sha256']['messages.json']}
    if raw.strip():
        code = helper.extract_code(raw)
        path = folder / ('fix_' + entry['case'].removeprefix('issue_') + '.py')
        atomic_text(path, code)
        state.update(fix_created=True, fix_file=path.name, fix_sha256=sha(path.read_bytes()))
        try:
            # Syntax-only check: does not import Qiskit, run the fix, or judge correctness.
            compile(code, str(path), 'exec')
            state.update(syntax_check='OK', status='CREATED')
        except (SyntaxError, ValueError) as exc:
            state.update(syntax_check='ERROR', status='SYNTAX_ERROR', error=f'{type(exc).__name__}: {exc}')
    else:
        state['error'] = 'Empty response or refusal; no code file created.'
    if choice.get('finish_reason') != 'stop':
        state['status'] = 'INCOMPLETE_RESPONSE'
        state['error'] = f'finish_reason={choice.get("finish_reason")}; retained response must be reviewed. ' + state['error']
    write_json(folder / 'status.json', state)
    return state


def export_report(root, model, manifest):
    report = root / model / 'reports' / 'generation_report.csv'
    rows = []
    for entry in manifest['cases']:
        path = root / model / 'generation' / entry['case'] / 'status.json'
        state = read_json(path) if path.is_file() else {}
        rows.append({'Case Number': entry['case'], 'Fix Created': 'Yes' if state.get('fix_created') else 'No',
                     'Error': state.get('error', ''), 'Generation Status': state.get('status', 'NOT STARTED'),
                     'Syntax Check': state.get('syntax_check', 'NOT CHECKED'), 'Model': model,
                     'Reasoning Effort': 'medium', 'Completed UTC': state.get('completed_utc', ''),
                     'Fix File': str(path.parent / state['fix_file']) if state.get('fix_file') else ''})
    text = io.StringIO(newline='')
    writer = csv.DictWriter(text, fieldnames=list(rows[0]))
    writer.writeheader()
    # Prevent Excel from interpreting exception text as a formula.
    for row in rows:
        writer.writerow({k: ("'" + v if isinstance(v, str) and v.startswith(('=', '+', '-', '@')) else v)
                         for k, v in row.items()})
    try:
        atomic_text(report, '\ufeff' + text.getvalue())
    except PermissionError:
        print(f'Close Excel to refresh {report}; individual status.json files are safe.', flush=True)
    return Counter(row['Generation Status'] for row in rows)


def check_saved(root, model, manifest):
    errors = []
    for entry in manifest['cases']:
        folder = root / model / 'generation' / entry['case']
        path = folder / 'status.json'
        if not path.is_file():
            continue
        state = read_json(path)
        if state.get('model') != model or state.get('input_sha256') != entry['input_sha256']['messages.json']:
            errors.append(f'{entry["case"]}: model/input mismatch')
        if state.get('fix_created'):
            fix = folder / state['fix_file']
            if not fix.is_file() or sha(fix.read_bytes()) != state['fix_sha256']:
                errors.append(f'{entry["case"]}: saved fix is missing or changed')
        if (folder / 'request.json').is_file() and read_json(folder / 'request.json') != request_for(root, model, entry):
            errors.append(f'{entry["case"]}: saved request differs')
    if errors:
        raise RuntimeError('\n'.join(errors))


def run_generation(root, model, manifest, helper, client, key, limit=None, retry_api_errors=False):
    check_saved(root, model, manifest)
    attempted = 0
    export_report(root, model, manifest)
    for entry in manifest['cases']:
        folder = root / model / 'generation' / entry['case']
        status_path = folder / 'status.json'
        state = read_json(status_path) if status_path.is_file() else {}
        if state:
            if state.get('status') != 'API_ERROR' or not retry_api_errors:
                print(f'SKIP {entry["case"]}: {state["status"]}', flush=True)
                continue
        if (folder / 'response.json').is_file():
            finish_response(folder, entry, model, read_json(folder / 'response.json'), helper)
            export_report(root, model, manifest)
            continue
        # An interrupted request may already have incurred cost. Never silently resubmit it.
        if (folder / 'inflight.json').exists() and not retry_api_errors:
            print(f'PAUSED {entry["case"]}: interrupted request. Review before --retry-api-errors.', flush=True)
            break
        if limit is not None and attempted >= limit:
            break
        folder.mkdir(parents=True, exist_ok=True)
        request = request_for(root, model, entry)
        write_json(folder / 'request.json', request)
        write_json(folder / 'inflight.json', {'started_utc': utcnow(), 'model': model, 'case': entry['case']})
        attempted += 1
        print(f'Processing {model} / {entry["case"]} ...', flush=True)
        try:
            response = client.chat.completions.create(**request)
        except Exception as exc:
            error = redact_error(exc, key)
            state = {'case': entry['case'], 'model': model, 'reasoning_effort': 'medium',
                     'status': 'API_ERROR', 'fix_created': False, 'error': error,
                     'input_sha256': entry['input_sha256']['messages.json'], 'completed_utc': utcnow()}
            write_json(status_path, state)
            with (folder / 'api_errors.jsonl').open('a', encoding='utf-8') as handle:
                handle.write(json.dumps(state) + '\n')
            (folder / 'inflight.json').unlink(missing_ok=True)
            export_report(root, model, manifest)
            print(error, flush=True)
            if getattr(exc, 'status_code', None) in (400, 401, 403, 404, 429):
                print('Stopping this model: check access, request settings, or quota before retrying.', flush=True)
                break
            continue
        # Save the untouched API response before extraction/syntax checking.
        write_json(folder / 'response.json', response.model_dump(mode='json'))
        state = finish_response(folder, entry, model, read_json(folder / 'response.json'), helper)
        (folder / 'inflight.json').unlink(missing_ok=True)
        export_report(root, model, manifest)
        print(f'{entry["case"]}: {state["status"]}', flush=True)
    check_saved(root, model, manifest)
    counts = export_report(root, model, manifest)
    print(f'{model}: {dict(counts)}', flush=True)
    print(f'Report: {root / model / "reports" / "generation_report.csv"}', flush=True)
    return counts


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root', type=Path, default=Path(__file__).resolve().parent)
    ap.add_argument('--model', required=True)
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument('--preflight', action='store_true', help='Offline input/hash checks; no API calls')
    mode.add_argument('--check-access', action='store_true', help='Retrieve model metadata with the current API key')
    mode.add_argument('--status', action='store_true', help='Verify saved artifacts and refresh CSV; no API calls')
    ap.add_argument('--limit', type=int, help='Maximum new requests for a small first run')
    ap.add_argument('--retry-api-errors', action='store_true', help='Explicitly retry API/interrupted requests; may incur cost')
    args = ap.parse_args()
    root = args.root.resolve()
    manifest, helper = load_experiment(root)
    if args.model not in manifest['new_models']:
        ap.error('Use exactly one of: ' + ', '.join(manifest['new_models']))
    if args.limit is not None and args.limit < 1:
        ap.error('--limit must be positive')
    if args.preflight:
        check_saved(root, args.model, manifest)
        print(f'OFFLINE OK: {args.model}, medium; 73 identical prompt inputs; 1015 assigned case/version pairs.')
        print('No credentials read, no API requests made, no generated files executed.')
        return
    if args.status:
        check_saved(root, args.model, manifest)
        print(dict(export_report(root, args.model, manifest)))
        return
    key = os.environ.get('OPENAI_API_KEY', '').strip()
    if not key:
        raise RuntimeError('OPENAI_API_KEY is not set in this PowerShell session. Run .\\set_api_key.ps1')
    from openai import OpenAI
    client = OpenAI(api_key=key, max_retries=2, timeout=600.0)
    if args.check_access:
        try:
            model = client.models.retrieve(args.model)
            print(f'Model metadata accessible: {model.id}. Generation/medium support is verified by the first real request.')
        except Exception as exc:
            raise RuntimeError(redact_error(exc, key)) from None
        return
    lock = root / args.model / 'generation.lock'
    try:
        with lock.open('x', encoding='utf-8') as handle:
            json.dump({'pid': os.getpid(), 'started_utc': utcnow()}, handle)
    except FileExistsError:
        raise RuntimeError(f'Another run may be active. Check the PID in {lock} before removing a stale lock.') from None
    try:
        counts = run_generation(root, args.model, manifest, helper, client, key, args.limit, args.retry_api_errors)
    finally:
        lock.unlink(missing_ok=True)
    if any(name not in ('CREATED', 'NOT STARTED') for name in counts):
        sys.exit(1)


if __name__ == '__main__':
    main()
