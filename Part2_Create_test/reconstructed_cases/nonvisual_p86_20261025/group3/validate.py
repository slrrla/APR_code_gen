from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from build_tests import TESTS, ROOT

HERE = Path(__file__).resolve().parent
ENVROOT = ROOT.parents[1] / 'Part1_Create_code' / 'envs'

def run(job):
    number, version, variant = job
    case = 'issue_' + number
    prefix = ENVROOT / ('qiskit_' + version.replace('.','_'))
    env = os.environ.copy()
    env.update(MUT=str(ROOT/case/(variant+'.py')), PYTHONIOENCODING='utf-8', PYTHONDONTWRITEBYTECODE='1',
               OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1', QISKIT_PARALLEL='FALSE', MPLBACKEND='Agg')
    env['PATH'] = os.pathsep.join(map(str,[prefix,prefix/'Library/bin',prefix/'Scripts'])) + os.pathsep + env['PATH']
    start=time.monotonic()
    record={'case':case,'version':version,'variant':variant}
    log=HERE/'logs'/case/version/(variant+'.log')
    log.parent.mkdir(parents=True,exist_ok=True)
    try:
        p=subprocess.run([str(prefix/'python.exe'),'-X','utf8',str(ROOT/case/'test.py')],cwd=HERE,env=env,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=150)
        output=p.stdout+'\n'+p.stderr
        record.update(returncode=p.returncode,status='PASS' if p.returncode==0 else ('FAIL' if 'AssertionError' in output else 'ERROR'))
    except subprocess.TimeoutExpired as e:
        record.update(status='TIMEOUT',returncode=None)
        output=str(e.stdout)+'\n'+str(e.stderr)
    log.write_text(output,encoding='utf-8')
    record.update(log=str(log),seconds=round(time.monotonic()-start,3))
    print(case,version,variant,record['status'],flush=True)
    return record

if __name__=='__main__':
    arguments=sys.argv[1:]
    version='0.46.3'
    if arguments and arguments[0].startswith('v='):
        version=arguments.pop(0)[2:]
    numbers=arguments or list(TESTS)
    jobs=[(number,version,variant) for number in numbers for variant in ('fixed','buggy')]
    path=HERE/'results.json'
    results=json.loads(path.read_text(encoding='utf-8')) if path.exists() else []
    targets={('issue_'+number,version,variant) for number,version,variant in jobs}
    results=[r for r in results if (r['case'],r['version'],r['variant']) not in targets]
    with ThreadPoolExecutor(max_workers=3) as pool:
        for future in as_completed([pool.submit(run,job) for job in jobs]):
            results.append(future.result())
            (HERE/'results.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
