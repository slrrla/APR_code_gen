"""Selection, isolated differential execution, and auditable reports for the P rows."""
import argparse
import ast
import csv
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent
ENV_ROOT = ROOT.parent.parent / 'Part1_Create_code' / 'envs'
WORKBOOK = Path('C:/Users/haha9/Downloads/non-visual_cases_161_(pass-pass).xlsx')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(name, data):
    (BASE / name).write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')


def prepare():
    import openpyxl
    workbook = openpyxl.load_workbook(WORKBOOK, data_only=True, read_only=True)
    sheet = workbook.active
    cases = []
    for rownum, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), 2):
        if str(row[2]).strip().lower() != 'p':
            continue
        raw = str(row[0])
        number = int(float(re.match(r'[0-9.]+', raw).group()))
        suffix = re.search(r'\((SE|SO)\)', raw, re.I)
        name = 'issue_%03d' % number + ('_' + suffix.group(1).lower() if suffix else '')
        directory = ROOT / name
        assert directory.is_dir(), name
        cases.append({'case': name, 'source_dir': str(directory), 'sheet': sheet.title,
                      'row': rownum, 'marker_cell': 'C%d' % rownum,
                      'versions': [v.strip() for v in str(row[7]).split(',') if v.strip()],
                      'difference_note': row[8],
                      'source_hashes': {v: digest(directory / (v + '.py')) for v in ('buggy', 'fixed')},
                      'preexisting_test_sha256': digest(directory / 'test.py') if (directory / 'test.py').exists() else None})
    save('selection.json', {'workbook': str(WORKBOOK), 'workbook_sha256': digest(WORKBOOK),
                            'selection': 'trim/lower(C) == p; exact SE/SO suffix from A', 'count': len(cases), 'cases': cases})
    print('Selected', len(cases), 'cases')


def environment(version):
    prefix = ENV_ROOT / ('qiskit_' + version.replace('.', '_'))
    env = os.environ.copy()
    env.update(PYTHONIOENCODING='utf-8', PYTHONDONTWRITEBYTECODE='1',
               OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1',
               NUMEXPR_NUM_THREADS='1', QISKIT_PARALLEL='FALSE', MPLBACKEND='Agg')
    env['PATH'] = os.pathsep.join(str(prefix / p) for p in ('', 'Library/bin', 'Scripts')) + os.pathsep + env['PATH']
    return prefix / 'python.exe', env


def probe(version):
    interpreter, env = environment(version)
    code = ('import sys,json,qiskit,importlib.metadata as m; '
            'names=["qiskit","qiskit-terra","qiskit-aer","numpy","scipy"]; '
            'd={x:(m.version(x) if list(m.distributions(name=x)) else None) for x in names}; '
            'd.update(python=sys.version,core=qiskit.__version__,interpreter=sys.executable); print(json.dumps(d))')
    try:
        proc = subprocess.run([str(interpreter), '-c', code], env=env, capture_output=True, text=True, timeout=30)
        if proc.returncode:
            raise RuntimeError(proc.stderr)
        data = json.loads(proc.stdout)
        data['ok'] = data['qiskit'] == version
        data['requested'] = version
        return data
    except Exception as exc:
        return {'ok': False, 'requested': version, 'interpreter': str(interpreter), 'error': str(exc)}


def run_one(case, version, variant, timeout):
    source = ROOT / case['case'] / (variant + '.py')
    test = source.parent / 'test.py'
    record = {'case': case['case'], 'version': version, 'variant': variant,
              'source_sha256': digest(source), 'test_sha256': digest(test)}
    interpreter, env = environment(version)
    env['MUT'] = str(source)
    started = time.monotonic()
    output = ''
    try:
        work_root = BASE / 'work'
        work_root.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='p86_', dir=work_root, ignore_cleanup_errors=True) as work:
            env.update(HOME=work, USERPROFILE=work, IPYTHONDIR=str(Path(work) / '.ipython'))
            process = subprocess.run([str(interpreter), '-X', 'utf8', str(test)], env=env,
                                     cwd=work, capture_output=True, text=True, encoding='utf-8',
                                     errors='replace', timeout=timeout)
            output = process.stdout + '\n' + process.stderr
            ran = re.search(r'Ran (\d+) tests?', output)
            record['tests_run'] = int(ran.group(1)) if ran else 0
            record['returncode'] = process.returncode
            if 'skipped=' in output:
                status = 'SKIP'
            elif process.returncode == 0:
                status = 'PASS' if ran and int(ran.group(1)) else 'INVALID_RUN'
            elif 'AssertionError' in output:
                status = 'FAIL'
            else:
                status = 'ERROR'
            errors = [line.strip() for line in output.splitlines()
                      if re.match(r'^(?:[\w.]*Error|AssertionError|unittest.case.SkipTest):', line)]
            record.update(status=status, detail='; '.join(dict.fromkeys(errors))[-2200:])
    except subprocess.TimeoutExpired as exc:
        output = str(exc.stdout or '') + '\n' + str(exc.stderr or '')
        record.update(status='TIMEOUT', detail=str(timeout) + ' second timeout')
    except Exception as exc:
        record.update(status='ENVIRONMENT_ERROR', detail=repr(exc))
    record['seconds'] = round(time.monotonic() - started, 3)
    log = BASE / 'logs' / case['case'] / version / (variant + '.log')
    log.parent.mkdir(parents=True, exist_ok=True)
    log.write_text(output, encoding='utf-8')
    record['log'] = str(log)
    print(record['case'], version, variant, record['status'], flush=True)
    return record


def run(args):
    selection = json.loads((BASE / 'selection.json').read_text(encoding='utf-8'))
    versions = sorted({v for c in selection['cases'] for v in c['versions']})
    probes = {v: probe(v) for v in versions}
    save('environments.json', probes)
    jobs = [(c, v, variant) for c in selection['cases']
            if not args.cases or c['case'] in args.cases
            for v in c['versions'] if not args.versions or v in args.versions
            for variant in ('buggy', 'fixed')]
    old = json.loads((BASE / 'results.json').read_text(encoding='utf-8')) if (BASE / 'results.json').exists() else []
    if args.resume:
        current = {(r['case'], r['version'], r['variant']): r for r in old}
        jobs = [(c, v, variant) for c, v, variant in jobs
                if not ((c['case'], v, variant) in current
                        and current[(c['case'], v, variant)]['test_sha256'] == digest(ROOT / c['case'] / 'test.py')
                        and current[(c['case'], v, variant)]['source_sha256'] == digest(ROOT / c['case'] / (variant + '.py'))
                        and current[(c['case'], v, variant)]['status'] not in ('ENVIRONMENT_ERROR', 'INVALID_RUN'))]
    keys = {(c['case'], v, variant) for c, v, variant in jobs}
    results = [r for r in old if (r['case'], r['version'], r['variant']) not in keys]
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        pending = [pool.submit(run_one, c, v, variant, args.timeout) for c, v, variant in jobs]
        for future in as_completed(pending):
            results.append(future.result())
            save('results.json', results)
    print('Finished', len(jobs), 'executions')


def report():
    selection = json.loads((BASE / 'selection.json').read_text(encoding='utf-8'))
    results = json.loads((BASE / 'results.json').read_text(encoding='utf-8'))
    rows = []
    audit = []
    version_rows = []
    index = {(r['case'], r['version'], r['variant']): r for r in results}
    for case in selection['cases']:
        name = case['case']
        path = ROOT / name / 'test.py'
        ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
        for variant, baseline in case['source_hashes'].items():
            assert digest(path.parent / (variant + '.py')) == baseline, 'Source changed: ' + name
        entries = [r for r in results if r['case'] == name]
        for entry in entries:
            assert entry['test_sha256'] == digest(path), 'Stale test result: ' + name
            assert entry['source_sha256'] == case['source_hashes'][entry['variant']], 'Stale source result: ' + name
        differential = []
        for version in case['versions']:
            for variant in ('buggy', 'fixed'):
                assert (name, version, variant) in index, 'Missing execution: ' + name + ' ' + version + ' ' + variant
            pair = {r['variant']: r for r in entries if r['version'] == version}
            separates = pair.get('fixed', {}).get('status') == 'PASS' and pair.get('buggy', {}).get('status') in ('FAIL', 'ERROR')
            if separates:
                differential.append(version)
            version_rows.append({'case': name, 'version': version, 'buggy': pair['buggy']['status'],
                                 'fixed': pair['fixed']['status'], 'differential': separates,
                                 'buggy_detail': pair['buggy'].get('detail', ''),
                                 'fixed_detail': pair['fixed'].get('detail', ''),
                                 'buggy_log': pair['buggy']['log'], 'fixed_log': pair['fixed']['log']})
        rows.append({'case': name, 'sheet_row': case['row'], 'test': str(path),
                     'differential_versions': ', '.join(differential),
                     'status': 'DIFFERENTIAL' if differential else 'REVIEW',
                     'fixed_results': '; '.join(r['version'] + ':' + r['status'] for r in entries if r['variant'] == 'fixed'),
                     'buggy_results': '; '.join(r['version'] + ':' + r['status'] for r in entries if r['variant'] == 'buggy')})
        audit.append({'case': name, 'test_sha256': digest(path), 'sources_unchanged': True,
                      'preexisting_test_unchanged': case['preexisting_test_sha256'] == digest(path) if case['preexisting_test_sha256'] else None})
    with (BASE / 'summary.csv').open('w', newline='', encoding='utf-8-sig') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    with (BASE / 'version_results.csv').open('w', newline='', encoding='utf-8-sig') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(version_rows[0]))
        writer.writeheader()
        writer.writerows(version_rows)
    save('audit.json', {'workbook_unchanged': digest(WORKBOOK) == selection['workbook_sha256'],
                        'all_tests_parse': True, 'cases': audit})
    expected_count = sum(2 * len(c['versions']) for c in selection['cases'])
    assert len(results) == expected_count, 'Unexpected duplicate or extra executions'
    save('summary.json', {'cases': len(rows), 'differential': sum(r['status'] == 'DIFFERENTIAL' for r in rows),
                          'review': [r['case'] for r in rows if r['status'] == 'REVIEW'], 'executions': len(results),
                          'expected_executions': expected_count, 'version_pairs': len(version_rows),
                          'differential_version_pairs': sum(r['differential'] for r in version_rows),
                          'assertion_fail_pass_version_pairs': sum(r['buggy'] == 'FAIL' and r['fixed'] == 'PASS' for r in version_rows),
                          'exception_error_pass_version_pairs': sum(r['buggy'] == 'ERROR' and r['fixed'] == 'PASS' for r in version_rows),
                          'assertion_fail_pass_cases': sorted({r['case'] for r in version_rows if r['buggy'] == 'FAIL' and r['fixed'] == 'PASS'}),
                          'exception_error_pass_cases': sorted({r['case'] for r in version_rows if r['buggy'] == 'ERROR' and r['fixed'] == 'PASS'})})
    print((BASE / 'summary.json').read_text(encoding='utf-8'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['prepare', 'run', 'report'])
    parser.add_argument('--cases', nargs='*')
    parser.add_argument('--versions', nargs='*')
    parser.add_argument('--workers', type=int, default=4)
    parser.add_argument('--timeout', type=int, default=120)
    parser.add_argument('--resume', action='store_true', help='Keep completed runs whose source and test hashes still match.')
    arguments = parser.parse_args()
    {'prepare': prepare, 'run': lambda: run(arguments), 'report': report}[arguments.action]()
