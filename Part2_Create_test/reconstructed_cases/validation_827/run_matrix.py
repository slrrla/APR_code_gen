"""Run standalone MUT tests in every exact release listed by the source workbook."""
import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import time

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent
ENVS = ROOT.parent.parent / 'Part1_Create_code' / 'envs'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def environment(prefix):
    env = os.environ.copy()
    env.update(PYTHONIOENCODING='utf-8', PYTHONDONTWRITEBYTECODE='1',
               OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1',
               NUMEXPR_NUM_THREADS='1', QISKIT_PARALLEL='FALSE', MPLBACKEND='Agg')
    env.pop('PYTHONPATH', None)
    env['PATH'] = os.pathsep.join(str(p) for p in
                                (prefix, prefix / 'Library/bin', prefix / 'Scripts')) + os.pathsep + env['PATH']
    return env


def probe(version):
    prefix = ENVS / ('qiskit_' + version.replace('.', '_'))
    interpreter = prefix / 'python.exe'
    script = ('import sys,json,importlib.metadata as m;'
              "names=['qiskit','qiskit-terra','qiskit-aer','qiskit-ignis','numpy','scipy'];"
              "versions={d.metadata['Name'].lower():d.version for d in m.distributions()};"
              "print(json.dumps({'python':sys.version.split()[0],'interpreter':sys.executable,"
              "'packages':{name:versions.get(name) for name in names}}))")
    p = subprocess.run([str(interpreter), '-c', script], env=environment(prefix),
                       capture_output=True, text=True, encoding='utf-8', timeout=30)
    if p.returncode:
        raise RuntimeError('%s environment probe failed: %s' % (version, p.stderr))
    result = json.loads(p.stdout.strip())
    assert result['packages']['qiskit'] == version, (version, result)
    return result


def run_one(job):
    case, version, variant, source, info = job
    test = ROOT / case / 'test.py'
    prefix = Path(info['interpreter']).parent
    env = environment(prefix)
    env['MUT'] = str(source)
    record = dict(case=case, version=version, variant=variant,
                  source=str(source), test=str(test), source_sha256=sha(source),
                  test_sha256=sha(test), environment=info)
    command = [info['interpreter'], '-X', 'utf8', str(test), '-v']
    record['command'] = command
    started = time.monotonic()
    with tempfile.TemporaryDirectory(prefix='apr_missing6_') as work:
        env.update(USERPROFILE=work, HOME=work, IPYTHONDIR=str(Path(work) / '.ipython'))
        try:
            p = subprocess.run(command, cwd=work, env=env, capture_output=True,
                               text=True, encoding='utf-8', errors='replace', timeout=120)
            output = p.stdout + '\n' + p.stderr
            count = re.search(r'Ran (\d+) tests?', output)
            record.update(returncode=p.returncode, tests_run=int(count.group(1)) if count else 0)
            if not p.returncode:
                record['status'] = 'PASS' if count and int(count.group(1)) > 0 and 'skipped=' not in output else 'INVALID_RUN'
            else:
                record['status'] = 'FAIL' if 'AssertionError:' in output else 'ERROR'
            record['detail'] = '; '.join(dict.fromkeys(line.strip() for line in output.splitlines()
                                                      if re.match(r'^(?:[\w.]*Error|AssertionError|unittest.case.SkipTest):', line)))[:2000]
        except subprocess.TimeoutExpired as error:
            output = str(error.stdout or '') + '\n' + str(error.stderr or '')
            record.update(status='TIMEOUT', returncode=None, tests_run=0, detail='120 seconds')
    record['seconds'] = round(time.monotonic() - started, 3)
    log = BASE / 'logs' / case / version / (variant + '.log')
    log.parent.mkdir(parents=True, exist_ok=True)
    log.write_text(output, encoding='utf-8')
    record['log'] = str(log)
    print(case, version, variant, record['status'], flush=True)
    return record


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--workers', type=int, default=4)
    args = parser.parse_args()
    selection = json.loads((BASE / 'selection.json').read_text(encoding='utf-8'))
    versions = sorted({v for case in selection['cases'] for v in case['versions']},
                      key=lambda v: tuple(map(int, v.split('.'))))
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        infos = dict(zip(versions, pool.map(probe, versions)))
    (BASE / 'environments.json').write_text(json.dumps(infos, indent=2), encoding='utf-8')
    jobs = []
    for case in selection['cases']:
        name = case['case']
        test = ROOT / name / 'test.py'
        if not test.is_file():
            raise FileNotFoundError(test)
        snapshot = BASE / 'tests' / name / 'test.py'
        snapshot.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(test, snapshot)
        sources = {'buggy': ROOT / name / 'buggy.py', 'fixed': ROOT / name / 'fixed.py'}
        alternative = ROOT / 'failpass_fixes' / ('case_%d_new_fix.py' % int(name.split('_')[1]))
        if alternative.is_file():
            sources['new_fix'] = alternative
        for version in case['versions']:
            jobs.extend((name, version, variant, source, infos[version]) for variant, source in sources.items())
    results = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        for future in as_completed([pool.submit(run_one, job) for job in jobs]):
            results.append(future.result())
            (BASE / 'results.json').write_text(json.dumps(results, indent=2), encoding='utf-8')
    assert len(results) == len(jobs)
    assert len({(r['case'], r['version'], r['variant']) for r in results}) == len(jobs)
    assert all(Path(r['log']).is_file() and r['test_sha256'] == sha(Path(r['test']))
               and r['source_sha256'] == sha(Path(r['source'])) for r in results)
    original = json.loads((BASE / 'source_hashes_before.json').read_text(encoding='utf-8'))
    assert all(sha(Path(p)) == digest for p, digest in original.items()), 'A target source was changed'
    summary = []
    for case in selection['cases']:
        counts = Counter((r['variant'], r['status']) for r in results if r['case'] == case['case'])
        row = dict(case=case['case'], versions=len(case['versions']),
                   outcomes=[dict(variant=variant, status=status, count=count)
                             for (variant, status), count in sorted(counts.items())])
        summary.append(row)
    (BASE / 'summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
    print(json.dumps(summary, indent=2))
    print('Verified %d executions; source/test hashes and exact release metadata recorded.' % len(results))


if __name__ == '__main__':
    main()
