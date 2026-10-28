"""Isolated fixed/buggy validation; no source rewriting or environment mutation."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import time

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
ENVS = ROOT.parents[1] / 'Part1_Create_code' / 'envs'
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def run(job):
    item, variant = job
    name = item['case']
    version = item.get('version') or ('2_5_0' if name in {'issue_018_so', 'issue_023', 'issue_050', 'issue_117', 'issue_133'} else '0_46_3')
    prefix = ENVS / ('qiskit_' + version)
    interpreter = prefix / 'python.exe'
    source = ROOT / name / (variant+'.py')
    test = ROOT / name / 'test.py'
    env = os.environ.copy()
    env.update(MUT=str(source), PYTHONDONTWRITEBYTECODE='1', PYTHONIOENCODING='utf-8',
               OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1',
               QISKIT_PARALLEL='FALSE', MPLBACKEND='Agg')
    env['PATH'] = os.pathsep.join(map(str,[prefix,prefix/'Library/bin',prefix/'Scripts'])) + os.pathsep + env['PATH']
    command = [str(interpreter), '-B', '-X', 'utf8', str(test), '-v']
    record = dict(case=name, variant=variant, version=version.replace('_','.'), command=command,
                  source=str(source), test=str(test), source_sha256=sha(source), test_sha256=sha(test))
    start = time.monotonic()
    with tempfile.TemporaryDirectory(prefix='nonvisual_group1_') as work:
        env.update(HOME=work, USERPROFILE=work, IPYTHONDIR=str(Path(work)/'.ipython'))
        try:
            p = subprocess.run(command,cwd=work,env=env,capture_output=True,text=True,
                               encoding='utf-8',errors='replace',timeout=240 if name=='issue_015' else 100)
            output = p.stdout+'\n'+p.stderr
            record['returncode'] = p.returncode
            record['status'] = ('PASS' if p.returncode==0 else 'FAIL' if 'AssertionError' in output else 'ERROR')
            if p.returncode==0 and (not re.search(r'Ran [1-9]\d* tests?',output) or re.search(r'skipped=\d',output)):
                record['status']='INVALID_RUN'
        except subprocess.TimeoutExpired as e:
            output = str(e.stdout)+'\n'+str(e.stderr)
            record.update(returncode=None,status='TIMEOUT')
    record['seconds']=round(time.monotonic()-start,3)
    log = OUT/'logs'/name/(variant+'.log')
    log.parent.mkdir(parents=True,exist_ok=True)
    log.write_text(output,encoding='utf-8')
    record['log']=str(log)
    record['source_unchanged'] = sha(source)==record['source_sha256']
    record['detail'] = '\n'.join(output.splitlines()[-7:])
    print(name,variant,record['status'],record['seconds'],flush=True)
    return record

def main():
    manifest = json.loads((OUT/'tests_manifest.json').read_text())
    selected = set(sys.argv[1:])
    if selected:
        manifest = [item for item in manifest if item['case'] in selected]
    jobs = [(item,variant) for item in manifest for variant in ('fixed','buggy')]
    results=[]
    if selected and (OUT/'results.json').exists():
        results = [row for row in json.loads((OUT/'results.json').read_text()) if row['case'] not in selected]
    with ThreadPoolExecutor(max_workers=3) as pool:
        for future in as_completed([pool.submit(run,job) for job in jobs]):
            results.append(future.result())
            (OUT/'results.json').write_text(json.dumps(results,indent=2),encoding='utf-8')

if __name__=='__main__':
    main()
