import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

case_dir = Path(r'C:\personal_webpage\my-portfolio\APR_code_gen\Part2_Create_test\reconstructed_cases\issue_096')
output_dir = Path(__file__).resolve().parent
python = Path(r'C:\Users\haha9\anaconda3\python.exe')
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
files = ['test.py', 'fixed.py', 'fixed_before.py', 'buggy.py', 'original_question.txt']
before = {name: sha(case_dir / name) for name in files}
results = []
for target in ['fixed.py', 'buggy.py', 'fixed_before.py']:
    label = target[:-3]
    runtime = output_dir / 'runtime' / label
    temp = runtime / 'temp'
    temp.mkdir(parents=True)
    env = os.environ.copy()
    env.update(MUT=str(case_dir / target), PYTHONDONTWRITEBYTECODE='1', PYTHONIOENCODING='utf-8', TEMP=str(temp), TMP=str(temp), USERPROFILE=str(runtime), HOME=str(runtime), IPYTHONDIR=str(runtime / '.ipython'))
    command = [str(python), str(case_dir / 'test.py'), '-v']
    start = time.monotonic()
    try:
        completed = subprocess.run(command, cwd=runtime, env=env, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=120)
        stdout, stderr = completed.stdout, completed.stderr
        code = completed.returncode
        duration = time.monotonic() - start
        match = re.search(r'Ran (\d+) tests? in', stderr)
        tests = int(match.group(1)) if match else 0
        failed = re.search(r'FAILED \(([^)]+)\)', stderr)
        counts = dict((key, int(value)) for key, value in re.findall(r'(failures|errors|skipped)=(\d+)', failed.group(1) if failed else ''))
        status = 'PASS' if code == 0 and tests > 0 and not counts.get('skipped', 0) and re.search(r'^OK\s*$', stderr, re.M) else 'FAIL' if counts.get('failures', 0) else 'ERROR' if code else 'INVALID_RUN'
    except subprocess.TimeoutExpired as error:
        stdout = error.stdout.decode('utf-8', 'replace') if isinstance(error.stdout, bytes) else error.stdout or ''
        stderr = error.stderr.decode('utf-8', 'replace') if isinstance(error.stderr, bytes) else error.stderr or ''
        code, duration, tests, counts, status = None, time.monotonic() - start, 0, {}, 'TIMEOUT'
    (output_dir / (label + '.stdout.log')).write_text(stdout, encoding='utf-8')
    (output_dir / (label + '.stderr.log')).write_text(stderr, encoding='utf-8')
    row = dict(target=str(case_dir / target), source_sha256=before[target], command=command, environment_overrides={k:env[k] for k in ['MUT','PYTHONDONTWRITEBYTECODE','PYTHONIOENCODING','TEMP','TMP','USERPROFILE','HOME','IPYTHONDIR']}, cwd=str(runtime), status=status, exit_code=code, tests_run=tests, failures=counts.get('failures',0), errors=counts.get('errors',0), skipped=counts.get('skipped',0), duration_seconds=duration, stdout_log=str(output_dir/(label+'.stdout.log')), stderr_log=str(output_dir/(label+'.stderr.log')))
    row.update(variant=target, interpreter=str(python), test_sha256=before['test.py'], skips=row['skipped'], tests_passed=max(0, tests-row['failures']-row['errors']-row['skipped']))
    results.append(row)
    print(json.dumps({k:row[k] for k in ['target','status','exit_code','tests_run','failures','errors','skipped','duration_seconds']}), flush=True)
after = {name: sha(case_dir / name) for name in files}
summary = dict(case='issue_096', python_executable=str(python), python_version=sys.version, ipython_version=importlib.metadata.version('IPython'), runtime_note='Configuration-file tests use a disposable home and a real IPython subprocess. No Qiskit computation or installation is required.', source_sha256_before=before, source_sha256_after=after, sources_unchanged=before==after, results=results, limitations=['Results establish correctness against the existing three unittest cases only.'])
summary.update(interpreter=str(python), environment={'python':sys.version.split()[0], 'IPython':importlib.metadata.version('IPython'), 'Qiskit':'not used'}, source_unchanged=before==after)
(output_dir / 'summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
print('SUMMARY ' + str(output_dir / 'summary.json'), flush=True)


