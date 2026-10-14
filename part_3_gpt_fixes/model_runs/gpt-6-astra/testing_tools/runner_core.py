"""User-run offline tests. No API calls, package installation, or source edits."""
import argparse
import csv
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import openpyxl

ENVIRONMENTS = {
    '0.25.0': 'qiskit_0250', '0.25.1': 'qiskit_0251_exact',
    '0.25.2': 'qiskit_0252_exact', '0.25.3': 'qiskit_0253_exact',
    '0.45.0': 'qiskit_045', '0.45.1': 'qiskit_0451_exact',
    '0.45.2': 'qiskit_0452_exact', '0.45.3': 'qiskit_0453_exact',
    '0.46.0': 'qiskit_0460_exact', '0.46.1': 'qiskit_0461_exact',
    '0.46.2': 'qiskit_0462', '0.46.3': 'qiskit_0463',
    '1.0.0': 'qiskit_100', '1.0.1': 'qiskit_101_exact', '1.0.2': 'qiskit_102_exact',
    '1.1.0': 'qiskit_110_exact', '1.1.1': 'qiskit_111', '1.1.2': 'qiskit_112_exact',
    '1.2.0': 'qiskit_120_exact', '1.2.1': 'qiskit_121_exact', '1.2.2': 'qiskit_122_exact',
    '1.2.4': 'qiskit_124', '2.0.0': 'qiskit_200_exact', '2.2.0': 'qiskit_220_exact',
    '2.3.0': 'qiskit_230_exact', '2.4.0': 'qiskit_240_exact', '2.5.0': 'qiskit_250',
}
ROOT = Path.home() / 'Downloads' / 'APR_code_gen-main (3)' / 'APR_code_gen-main' / 'Part2_Create_test' / 'model_runs'
TEMPLATE = Path.home() / 'Downloads' / '73_cases_5.6_luna_fixes (3).xlsx'
VALID = Path.home() / 'Downloads' / 'Valid_Cases_104 (2).xlsx'


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def atomic_text(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + '.tmp')
    temp.write_text(text, encoding='utf-8')
    temp.replace(path)


def write_json(path, value):
    atomic_text(path, json.dumps(value, indent=2, ensure_ascii=False) + '\n')


def child_environment(py):
    env = os.environ.copy()
    for key in ('OPENAI_API_KEY', 'OPEN_AI_KEY'):
        env.pop(key, None)
    env['PYTHONIOENCODING'] = 'utf-8'
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    env['PYTHONNOUSERSITE'] = '1'
    env.pop('PYTHONHOME', None)
    env.pop('PYTHONPATH', None)
    home = py.parent
    env['PATH'] = os.pathsep.join([str(home), str(home / 'Scripts'), str(home / 'Library' / 'bin'), env.get('PATH', '')])
    env['CONDA_PREFIX'] = str(home)
    return env


def capture(command, *, cwd, env, timeout):
    """Stream to a file at the caller; kill only this launched process tree on timeout."""
    return subprocess.run(command, cwd=str(cwd), env=env, capture_output=True,
                          text=True, encoding='utf-8', errors='replace', timeout=timeout,
                          creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))


def make_plan(args):
    manifest = read_json(args.root / '_shared' / 'manifest.json')
    if args.model != 'gpt-6-luna':
        raise ValueError('This batch is intentionally restricted to gpt-6-luna.')
    entries = sorted(manifest['cases'], key=lambda e: int(re.search(r'\d+', e['case'])[0]))
    if args.all_cases:
        assert len(entries) == 73
    else:
        entries = entries[:35]
        assert len(entries) == 35 and entries[-1]['case'] == 'issue_596'
    valid = openpyxl.load_workbook(args.valid, data_only=True).worksheets[0]
    source = openpyxl.load_workbook(args.template, data_only=True)
    old_buggy = {}
    for row in source.worksheets[0].iter_rows(min_row=2, values_only=True):
        if isinstance(row[0], str) and row[0].startswith('issue_'):
            key = (row[0], row[1])
            if key in old_buggy:
                raise ValueError(f'Duplicate template row: {key}')
            old_buggy[key] = row[2]
    plan = []
    for entry in entries:
        case = entry['case']
        versions = re.findall(r'\d+\.\d+\.\d+', str(valid.cell(entry['valid_row'], 4).value))
        label = str(valid.cell(entry['valid_row'], 1).value)
        assert int(re.search(r'\d+', label)[0]) == int(re.search(r'\d+', case)[0])
        assert versions == entry['versions'], f'Valid_104 assignment changed: {case}'
        assert len(versions) == len(set(versions)) and all(v in ENVIRONMENTS for v in versions)
        case_dir = Path(entry['source_case_dir'])
        alternatives = [case_dir / n for n in ('new_test.py', 'new-test.py') if (case_dir / n).is_file()]
        if len(alternatives) > 1:
            raise ValueError(f'Two new-test alternatives exist in {case_dir}; choose one before running.')
        test = alternatives[0] if alternatives else case_dir / 'test.py'
        human = case_dir / 'fixed.py'
        generation = args.root / args.model / 'generation' / case
        state = read_json(generation / 'status.json')
        luna = generation / state['fix_file']
        for path in (test, human, luna):
            if not path.is_file():
                raise FileNotFoundError(path)
        assert state['model'] == args.model and state['status'] == 'CREATED'
        assert digest(luna) == state['fix_sha256'], f'Generated fix changed: {case}'
        assert state['input_sha256'] == entry['input_sha256']['messages.json']
        for version in versions:
            assert (case, version) in old_buggy, f'No recorded buggy result for {case}/{version}'
        plan.append({'case': case, 'versions': versions, 'test': str(test), 'test_sha256': digest(test),
                     'targets': {'HUMAN_FIXED': str(human), 'LUNA_FIXED': str(luna)},
                     'target_sha256': {'HUMAN_FIXED': digest(human), 'LUNA_FIXED': digest(luna)},
                     'buggy_recorded': {v: old_buggy[(case, v)] for v in versions}})
    assert sum(len(e['versions']) for e in plan) == (1015 if args.all_cases else 501)
    # Shared local helpers can affect tests, so record them along with the test files.
    helper_dir = Path(entries[0]['source_case_dir']).parent
    helpers = {str(p): digest(p) for p in sorted(helper_dir.glob('*oracle*.py'))}
    return {'model': args.model, 'cases': plan, 'helpers': helpers, 'timeout_seconds': args.timeout,
            'source_valid': str(args.valid), 'source_template': str(args.template),
            'classification': 'Log-based; flagged failures need manual question/oracle review.',
            'buggy_policy': 'Copied as recorded from template; not rerun.'}


def print_plan(plan):
    for e in plan['cases']:
        print(e['case'] + ' | ' + ', '.join(e['versions']) + ' | ' + Path(e['test']).name)
    pairs = sum(len(e['versions']) for e in plan['cases'])
    print(f'\n{len(plan["cases"])} cases; {pairs} case/version pairs; {2 * pairs} Human/Luna test processes.')
    print('Buggy results copied from reference workbook. No API calls, no source edits.')


def probe_environments(plan, env_root):
    versions = sorted({v for e in plan['cases'] for v in e['versions']}, key=lambda v: tuple(map(int, v.split('.'))))
    snapshots = {}
    code = ('import json,sys; from importlib.metadata import distributions; '
            'p={d.metadata["Name"].lower().replace("_","-"):d.version for d in distributions() if d.metadata["Name"]}; '
            'print(json.dumps({"python":sys.version,"packages":p}))')
    for version in versions:
        py = env_root / ENVIRONMENTS[version] / 'python.exe'
        if not py.is_file():
            raise FileNotFoundError(f'Missing assigned environment: {py}')
        env = child_environment(py)
        process = capture([str(py), '-B', '-c', code], cwd=py.parent, env=env, timeout=60)
        if process.returncode:
            raise RuntimeError(f'{version}: environment probe failed:\n{process.stdout}\n{process.stderr}')
        info = json.loads(process.stdout.strip())
        actual = info['packages'].get('qiskit')
        if actual != version:
            raise RuntimeError(f'{ENVIRONMENTS[version]} contains Qiskit {actual}, not {version}. No cases run.')
        check = capture([str(py), '-m', 'pip', 'check'], cwd=py.parent, env=env, timeout=60)
        if check.returncode:
            raise RuntimeError(f'{version}: dependency check failed. No cases run.\n{check.stdout}\n{check.stderr}')
        snapshots[version] = {'python_exe': str(py), **info}
        print(f'ENV OK: {version} / {ENVIRONMENTS[version]}', flush=True)
    return snapshots


def classify(exit_code, log, target, timed_out):
    """Categorize observed execution only; do not claim semantic correctness beyond the tests."""
    if timed_out:
        return 'ERROR', '(runtime error: runner timeout; process tree stopped. Inconclusive correctness; review runtime limit.)', True
    if exit_code is None:
        return 'NOT TESTED', 'Test process did not start; see launch error in the log.', True
    native = exit_code < 0 or exit_code >= 0x80000000
    if native or 'SIMULATOR_PROCESS_ERROR:' in log:
        return 'ERROR', f'(runtime error: native process/simulator crash; exit {exit_code}. Inspect the full log and environment.)', True
    count = re.findall(r'^Ran (\d+) tests? in ', log, re.M)
    if exit_code == 0:
        if count and int(count[-1]) > 0 and re.search(r'^OK\s*$', log, re.M):
            return 'PASS', f'The selected test completed successfully ({count[-1]} tests).', False
        return 'NOT TESTED', 'Exit 0 without a complete, unskipped unittest success; do not treat as a correctness PASS.', True
    # Use the exact target filename, not the presence of any arbitrary traceback.
    frames = re.findall(r'File "([^"]+)"', log)
    normalize = lambda s: os.path.normcase(os.path.abspath(s))
    target_frame = any(normalize(frame) == normalize(str(target)) for frame in frames)
    exceptions = re.findall(r'^((?:[\w.]+(?:Error|Exception)|AssertionError|SystemExit|KeyboardInterrupt):[^\r\n]*)', log, re.M)
    detail = ' / '.join(dict.fromkeys(exceptions))
    if not detail:
        failures = re.findall(r'^(?:FAIL|ERROR): (.+)', log, re.M)
        detail = '; '.join(failures) or f'Process exited with code {exit_code}; see log.'
    detail = detail[:700]
    if 'TimeoutExpired' in log:
        return 'ERROR', '(runtime error: ' + detail + ' Timeout may originate in the test; review required.)', True
    if target_frame:
        return 'ERROR', '(runtime error: ' + detail + ' Traceback includes the target program; review test guards/environment before attributing blame.)', True
    if not count or int(count[-1]) == 0:
        return 'ERROR', '(runtime error: ' + detail + ' Test setup did not complete; environment/test-harness review required.)', True
    return 'FAIL', ('Test failure: ' + detail + ' No target frame establishes a target execution exception. '
                    'Review output/interface expectations against the question.'), True


def kill_child(process):
    if process.poll() is not None:
        return
    if os.name == 'nt':
        subprocess.run(['taskkill', '/PID', str(process.pid), '/T', '/F'], capture_output=True,
                       creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
    else:
        process.kill()
    process.wait(timeout=30)


def execute_one(entry, version, target_name, env_info, batch, timeout):
    target = Path(entry['targets'][target_name])
    test = Path(entry['test'])
    py = Path(env_info['python_exe'])
    folder = batch / 'logs' / entry['case'] / version
    folder.mkdir(parents=True, exist_ok=True)
    log_path = folder / (target_name + '.txt')
    marker = folder / (target_name + '.inflight.json')
    env = child_environment(py)
    env['MUT'] = str(target)
    command = [str(py), '-B', '-u', '-X', 'utf8', str(test)]
    started = datetime.now(timezone.utc).isoformat()
    timer = time.monotonic()
    timed_out = False
    exit_code = None
    write_json(marker, {'started_utc': started, 'command': command, 'target': str(target)})
    with log_path.open('w', encoding='utf-8') as log:
        log.write(f'CASE={entry["case"]}\nQISKIT={version}\nTARGET={target}\nTEST={test}\n\n')
        log.flush()
        try:
            process = subprocess.Popen(command, cwd=str(test.parent), env=env, stdout=log, stderr=subprocess.STDOUT,
                                       creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
        except OSError as exc:
            log.write(f'LAUNCH_ERROR: {exc}\n')
        else:
            write_json(marker, {'started_utc': started, 'pid': process.pid, 'command': command, 'target': str(target)})
            try:
                exit_code = process.wait(timeout=timeout)
            except subprocess.TimeoutExpired:
                timed_out = True
                kill_child(process)
                exit_code = process.returncode
                log.write(f'\nRUNNER_TIMEOUT: {timeout} seconds\n')
            except KeyboardInterrupt:
                kill_child(process)
                log.write('\nINTERRUPTED: no result recorded; this test must be resumed.\n')
                raise
    text = log_path.read_text(encoding='utf-8', errors='replace')
    category, reason, review = classify(exit_code, text, target, timed_out)
    raw = 'NOT TESTED' if exit_code is None else ('PASS' if exit_code == 0 else 'FAIL')
    record = {'case': entry['case'], 'version': version, 'target': target_name,
              'exit_code': exit_code, 'raw_result': raw, 'classification': category, 'reason': reason,
              'review_required': review, 'seconds': round(time.monotonic() - timer, 3),
              'started_utc': started, 'test': str(test), 'test_sha256': digest(test),
              'target_file': str(target), 'target_sha256': digest(target),
              'log': str(log_path), 'log_sha256': digest(log_path), 'timed_out': timed_out}
    write_json(folder / (target_name + '.json'), record)
    marker.unlink(missing_ok=True)
    return record


def collected(plan, batch):
    data = []
    for entry in plan['cases']:
        for version in entry['versions']:
            for target in ('HUMAN_FIXED', 'LUNA_FIXED'):
                path = batch / 'logs' / entry['case'] / version / (target + '.json')
                if path.is_file():
                    row = read_json(path)
                    assert (row['case'], row['version'], row['target']) == (entry['case'], version, target)
                    assert row['test_sha256'] == entry['test_sha256']
                    assert row['target_sha256'] == entry['target_sha256'][target]
                    assert digest(Path(row['log'])) == row['log_sha256'], f'Log modified: {path}'
                    data.append(row)
    return data


def save_results(plan, batch, data=None):
    if data is None:
        data = collected(plan, batch)
    write_json(batch / 'results.json', {'plan': plan, 'records': data})
    columns = ['case', 'version', 'target', 'raw_result', 'exit_code', 'classification', 'reason',
               'review_required', 'seconds', 'test', 'target_file', 'log']
    stream = io.StringIO(newline='')
    writer = csv.DictWriter(stream, fieldnames=columns, extrasaction='ignore')
    writer.writeheader()
    for row in data:
        safe = {k: ("'" + v if isinstance(v, str) and v.startswith(('=', '+', '-', '@')) else v)
                for k, v in row.items()}
        writer.writerow(safe)
    atomic_text(batch / 'results.csv', '\ufeff' + stream.getvalue())
    return data


def export_workbook(batch):
    node = Path.home() / '.cache' / 'codex-runtimes' / 'codex-primary-runtime' / 'dependencies' / 'node' / 'bin' / 'node.exe'
    if not node.is_file():
        raise FileNotFoundError(f'Bundled Node missing: {node}. JSON/CSV/logs remain saved.')
    process = subprocess.run([str(node), str(Path(__file__).with_name('export_results.mjs')), str(batch / 'results.json')])
    if process.returncode:
        raise RuntimeError('Workbook export failed (possibly open in Excel). Logs and CSV are safe; use --report-only.')
    # Read-only independent reconciliation of the exported workbook and formula caches.
    path = batch / 'gpt_6_luna_first35_results.xlsx'
    wb = openpyxl.load_workbook(path, data_only=True)
    payload = read_json(batch / 'results.json')
    records = {(r['case'], r['version'], r['target']): r for r in payload['records']}
    cases = payload['plan']['cases']
    assert wb.sheetnames == ['Exit results', 'Detailed reasons', 'Summary']
    pairs = sum(len(e['versions']) for e in cases)
    assert wb.worksheets[0].max_row == pairs + 1
    count = Counter()
    rownum = 2
    for case in cases:
        for version in case['versions']:
            assert wb.worksheets[1].cell(rownum, 1).value == case['case']
            assert wb.worksheets[1].cell(rownum, 2).value == version
            for target, col in (('HUMAN_FIXED', 4), ('LUNA_FIXED', 6)):
                r = records.get((case['case'], version, target), {})
                expected = r.get('classification', 'NOT TESTED')
                assert wb.worksheets[1].cell(rownum, col).value == expected
                if target == 'LUNA_FIXED':
                    count[(case['case'], expected)] += 1
            rownum += 1
    for i, case in enumerate(cases, 2):
        expected = [count[(case['case'], s)] for s in ('PASS', 'ERROR', 'FAIL')]
        assert [wb['Summary'].cell(i, c).value for c in range(2, 6)] == [sum(expected), *expected]
    assert not any(c.data_type == 'e' for ws in wb for row in ws for c in row)
    print(f'Workbook verified against logs/records: {pairs} rows and all {len(cases)} case summaries reconcile.')


def check_extension(saved, proposed):
    old_cases = saved['cases']
    if len(old_cases) >= len(proposed['cases']):
        raise RuntimeError('Extension must add cases, not replace or remove them.')
    if proposed['cases'][:len(old_cases)] != old_cases:
        raise RuntimeError('Original case inputs/tests/versions changed. Cannot extend this batch.')
    if {k: v for k, v in saved.items() if k != 'cases'} != {k: v for k, v in proposed.items() if k != 'cases'}:
        raise RuntimeError('Original batch settings or shared helpers changed. Cannot extend this batch.')


def prepare_batch(batch, plan, snapshots, allow_extension):
    plan_path = batch / 'plan.json'
    env_path = batch / 'environments.json'
    if not plan_path.exists():
        if env_path.exists():
            raise RuntimeError('Environment snapshot exists without its plan. Inspect this batch before proceeding.')
        write_json(plan_path, plan)
        write_json(env_path, snapshots)
        return
    if not env_path.is_file() or read_json(env_path) != snapshots:
        raise RuntimeError('environments.json changed. Do not mix runs from different environments.')
    saved = read_json(plan_path)
    if saved == plan:
        return
    if not allow_extension:
        raise RuntimeError('Plan changed. To add remaining cases, use --all-cases --extend-plan; existing cases must be unchanged.')
    check_extension(saved, plan)
    existing = collected(saved, batch)
    backup = batch / 'backups' / ('before_extension_' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))
    backup.mkdir(parents=True)
    for name in ('plan.json', 'environments.json', 'results.json', 'results.csv', 'gpt_6_luna_first35_results.xlsx'):
        source = batch / name
        if source.is_file():
            shutil.copy2(source, backup / name)
    write_json(plan_path, plan)
    print(f'Extended plan: {len(saved["cases"])} -> {len(plan["cases"])} cases; {len(existing)} completed executions preserved.')
    print(f'Backup saved: {backup}')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root', type=Path, default=ROOT)
    ap.add_argument('--model', default='gpt-6-luna')
    ap.add_argument('--valid', type=Path, default=VALID)
    ap.add_argument('--template', type=Path, default=TEMPLATE)
    ap.add_argument('--env-root', type=Path, default=Path.home() / 'miniconda3' / 'envs')
    ap.add_argument('--batch', default='first35')
    ap.add_argument('--timeout', type=int, default=900)
    ap.add_argument('--max-runs', type=int)
    ap.add_argument('--all-cases', action='store_true', help='Include all 73 cases, with their individually assigned versions.')
    ap.add_argument('--extend-plan', action='store_true', help='Back up and extend an existing batch without changing its completed cases.')
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument('--plan', action='store_true')
    mode.add_argument('--preflight', action='store_true')
    mode.add_argument('--report-only', action='store_true')
    mode.add_argument('--run', action='store_true')
    ap.add_argument('--resume-interrupted', action='store_true')
    args = ap.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9_-]+', args.batch):
        ap.error('Batch must contain letters, digits, underscores or hyphens only.')
    if args.timeout < 1 or (args.max_runs is not None and args.max_runs < 1):
        ap.error('Timeout and max-runs must be positive.')
    plan = make_plan(args)
    if args.plan or not (args.preflight or args.report_only or args.run):
        print_plan(plan)
        return
    batch = args.root / args.model / 'testing' / args.batch
    if args.report_only:
        saved = read_json(batch / 'plan.json')
        if saved != plan:
            raise RuntimeError('Inputs/settings changed. Do not combine incompatible runs; preserve this batch.')
        save_results(saved, batch)
        export_workbook(batch)
        return
    snapshots = probe_environments(plan, args.env_root)
    if args.preflight:
        print('PREFLIGHT OK. Exact installed versions and pip dependency checks passed. No case tests run.')
        return
    batch.mkdir(parents=True, exist_ok=True)
    lock = batch / 'runner.lock'
    with lock.open('x', encoding='utf-8') as handle:
        json.dump({'pid': os.getpid(), 'started_utc': datetime.now(timezone.utc).isoformat()}, handle)
    try:
        prepare_batch(batch, plan, snapshots, args.extend_plan)
        # Verify all stored evidence before resuming, and skip every completed outcome.
        existing = collected(plan, batch)
        done = {(r['case'], r['version'], r['target']) for r in existing}
        attempted = 0
        total = 2 * sum(len(e['versions']) for e in plan['cases'])
        stop = False
        for entry in plan['cases']:
            if stop:
                break
            for version in entry['versions']:
                if stop:
                    break
                for target in ('HUMAN_FIXED', 'LUNA_FIXED'):
                    if (entry['case'], version, target) in done:
                        continue
                    if args.max_runs is not None and attempted >= args.max_runs:
                        stop = True
                        break
                    marker = batch / 'logs' / entry['case'] / version / (target + '.inflight.json')
                    if marker.exists() and not args.resume_interrupted:
                        raise RuntimeError(f'Interrupted test marker: {marker}. Check its PID, then use --resume-interrupted.')
                    if marker.exists():
                        # Keep partial output rather than silently overwriting it on resume.
                        log = marker.with_name(target + '.txt')
                        if log.exists():
                            archived = log.with_name(target + '.interrupted_' + str(time.time_ns()) + '.txt')
                            log.rename(archived)
                    print(f'\n[{len(done)+1}/{total}] {entry["case"]} / {version} / {target}', flush=True)
                    result = execute_one(entry, version, target, snapshots[version], batch, args.timeout)
                    attempted += 1
                    existing.append(result)
                    done.add((entry['case'], version, target))
                    print(f'{result["classification"]}; exit={result["exit_code"]}; {result["seconds"]} seconds', flush=True)
                    save_results(plan, batch, existing)
        data = save_results(plan, batch, existing)
        export_workbook(batch)
        print(f'Saved {len(data)}/{total} test executions to {batch}')
        print(Counter((r['target'], r['classification']) for r in data))
    except KeyboardInterrupt:
        save_results(plan, batch)
        print('\nStopped. Completed results saved. Use --report-only or resume after checking the interrupted marker.')
    finally:
        lock.unlink(missing_ok=True)


if __name__ == '__main__':
    main()
