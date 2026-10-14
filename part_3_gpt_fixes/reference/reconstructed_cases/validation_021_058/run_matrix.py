"""Verify existing/new oracles for buggy, fixed and correctly placed Luna files.

Each test executes in a fresh process. Pre-swap evidence is archived separately.
"""
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import time

ROOT = Path(__file__).resolve().parent.parent
ENV_ROOT = ROOT.parent.parent / 'Part1_Create_code' / 'envs'
SELECTION = ROOT.parent / 'test_validation' / 'batch01' / 'selection.json'
CASES = {'issue_021_se': 'test-new.py', 'issue_058_se': 'test_new.py'}
RESULTS_PATH = Path(__file__).resolve().parent/'results_hardened.json'
PROBE = '''import importlib.metadata as m, json, sys
import numpy, qiskit
from qiskit import Aer
def version(name):
    try: return m.version(name)
    except m.PackageNotFoundError: return None
print('__PROBE__' + json.dumps(dict(python=sys.version.split()[0], interpreter=sys.executable,
    qiskit=version('qiskit'), terra=version('qiskit-terra'), aer=version('qiskit-aer'),
    numpy=version('numpy'), core=qiskit.__version__)))
'''


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def environment(version):
    prefix = ENV_ROOT / ('qiskit_' + version.replace('.', '_'))
    env = os.environ.copy()
    for name in ('PYTHONPATH', 'PYTHONHOME', 'MUT'):
        env.pop(name, None)
    env.update(PYTHONIOENCODING='utf-8', PYTHONDONTWRITEBYTECODE='1',
               PYTHONNOUSERSITE='1', OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1',
               MKL_NUM_THREADS='1', QISKIT_PARALLEL='FALSE', MPLBACKEND='Agg')
    env['PATH'] = os.pathsep.join(map(str, [prefix, prefix/'Library/bin', prefix/'Scripts'])) + os.pathsep + env['PATH']
    return prefix/'python.exe', env


def probe(version):
    python, env = environment(version)
    completed = subprocess.run([str(python), '-X', 'utf8', '-c', PROBE], env=env,
                               capture_output=True, text=True, encoding='utf-8', timeout=60)
    if completed.returncode:
        raise RuntimeError(version + ': ' + completed.stderr)
    line = next(line for line in completed.stdout.splitlines() if line.startswith('__PROBE__'))
    info = json.loads(line[len('__PROBE__'):])
    assert info['qiskit'] == version, (version, info)
    return version, info


def run_one(case, version, suite, test_name, variant, source, info):
    python, env = environment(version)
    test = ROOT/case/test_name
    env['MUT'] = str(source)
    command = [str(python), '-X', 'utf8', str(test), '-v']
    record = dict(case=case, version=version, suite=suite, variant=variant,
                  source=str(source), test=str(test), source_sha256=sha(source),
                  test_sha256=sha(test), command=command, packages=info,
                  observer_sha256=sha(ROOT/'simulation_oracle.py') if suite=='new' else None,
                  executed_at_utc=datetime.now(timezone.utc).isoformat())
    started = time.monotonic()
    with tempfile.TemporaryDirectory(prefix='apr_021_058_') as work:
        env.update(USERPROFILE=work, HOME=work, IPYTHONDIR=str(Path(work)/'.ipython'))
        try:
            p = subprocess.run(command, cwd=work, env=env, capture_output=True, text=True,
                               encoding='utf-8', errors='replace', timeout=120)
            stdout, stderr = p.stdout, p.stderr
            output = stdout + '\n' + stderr
            match = re.search(r'Ran (\d+) tests?', output)
            tests_run = int(match.group(1)) if match else 0
            if p.returncode == 0:
                status = 'PASS' if tests_run > 0 and re.search(r'^OK\s*$', output, re.M) else 'INVALID_RUN'
            elif re.search(r'^FAIL:', output, re.M):
                status = 'FAIL'
            else:
                status = 'ERROR'
            errors = [line.strip() for line in output.splitlines()
                      if re.match(r'^(?:[\w.]*Error|AssertionError|unittest.case.SkipTest):', line)]
            record.update(status=status, returncode=p.returncode, tests_run=tests_run,
                          detail='; '.join(dict.fromkeys(errors)))
        except subprocess.TimeoutExpired as exc:
            stdout = (exc.stdout or b'').decode('utf-8', errors='replace') if isinstance(exc.stdout, bytes) else (exc.stdout or '')
            stderr = (exc.stderr or b'').decode('utf-8', errors='replace') if isinstance(exc.stderr, bytes) else (exc.stderr or '')
            record.update(status='TIMEOUT', returncode=None, tests_run=None, detail='120 second timeout')
    record['seconds'] = round(time.monotonic()-started, 3)
    log = ROOT/case/'test_results_logs'/version/(suite+'_'+variant+'.log')
    log.parent.mkdir(parents=True, exist_ok=True)
    log.write_text('COMMAND: '+json.dumps(command)+'\nMUT: '+str(source)+'\n\nSTDOUT:\n'+stdout+'\nSTDERR:\n'+stderr, encoding='utf-8')
    record['log'] = str(log)
    return record


def main():
    selection = json.loads(SELECTION.read_text(encoding='utf-8'))
    versions = {c['case']: c['versions'] for c in selection['cases'] if c['case'] in CASES}
    assert set(versions) == set(CASES)
    probes = {}
    with ThreadPoolExecutor(max_workers=4) as pool:
        for future in as_completed([pool.submit(probe, v) for v in sorted(set(sum(versions.values(), [])))]):
            version, info = future.result()
            probes[version] = info
            print('PROBED', version, info, flush=True)
    (Path(__file__).parent/'environments.json').write_text(json.dumps(probes, indent=2), encoding='utf-8')
    results = []
    with ThreadPoolExecutor(max_workers=4) as pool:
        jobs = []
        for case, new_test in CASES.items():
            for version in versions[case]:
                for suite, test_name in [('old', 'test.py'), ('new', new_test)]:
                    targets = [(v, ROOT/case/(v+'.py')) for v in ('buggy', 'fixed', 'fixed_luna')]
                    for variant, source in targets:
                        jobs.append(pool.submit(run_one, case, version, suite, test_name, variant, source, probes[version]))
        for index, future in enumerate(as_completed(jobs), 1):
            record = future.result()
            results.append(record)
            print(index, '/', len(jobs), record['case'], record['version'], record['suite'],
                  record['variant'], record['status'], record['detail'][:200], flush=True)
    expected = {(c, v, s, k) for c in CASES for v in versions[c] for s in ('old', 'new')
                for k in ('buggy', 'fixed', 'fixed_luna')}
    assert {(r['case'], r['version'], r['suite'], r['variant']) for r in results} == expected
    assert len(results) == len(expected)
    for record in results:
        assert sha(Path(record['source'])) == record['source_sha256']
        assert sha(Path(record['test'])) == record['test_sha256']
        if record['suite'] == 'new':
            assert sha(ROOT/'simulation_oracle.py') == record['observer_sha256']
        if record['status'] == 'PASS':
            assert record['returncode'] == 0 and record['tests_run'] == 1
    # Save once after verification. Repeated truncation was vulnerable to a
    # transient Windows file-sharing error while a viewer read the aggregate.
    payload = json.dumps(results, indent=2)
    for attempt in range(5):
        try:
            RESULTS_PATH.write_text(payload, encoding='utf-8')
            break
        except OSError:
            if attempt == 4:
                raise
            time.sleep(0.1)
    for case in CASES:
        records = [r for r in results if r['case'] == case]
        (ROOT/case/'test_results_details.json').write_text(json.dumps(records, indent=2), encoding='utf-8')
        print('SUMMARY', case, Counter((r['suite'], r['variant'], r['status']) for r in records), flush=True)
    print('VERIFIED', len(results), 'executions', flush=True)
    print('RESULTS', RESULTS_PATH, flush=True)


if __name__ == '__main__':
    main()
