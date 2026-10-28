from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import hashlib
import json
import os
import re
import subprocess
import tempfile
import time
import openpyxl

BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[1]
ENVROOT=ROOT.parents[1]/'Part1_Create_code'/'envs'
CASES=['139','147','151','152','162','163','165','171','191','199','201','221','271','275','316','334','346','347','364','377','401','406']
versions={}
for row in openpyxl.load_workbook(r'C:\Users\haha9\Downloads\non-visual_cases_161_(pass-pass).xlsx',data_only=True).active.iter_rows(min_row=2,values_only=True):
    if row[0] is not None:
        versions[str(row[0]).removesuffix('.0')]=str(row[7] or '').split(',')[0].strip()

def run(job):
    number,variant=job
    version=versions[number]
    prefix=ENVROOT/('qiskit_'+version.replace('.','_'))
    py=prefix/'python.exe'
    source=ROOT/('issue_'+number)/(variant+'.py')
    test=source.with_name('test.py')
    env=os.environ.copy()
    env.update(MUT=str(source),PYTHONIOENCODING='utf-8',PYTHONDONTWRITEBYTECODE='1',OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',QISKIT_PARALLEL='FALSE',MPLBACKEND='Agg')
    env['PATH']=os.pathsep.join(map(str,[prefix,prefix/'Library'/'bin',prefix/'Scripts']))+os.pathsep+env['PATH']
    start=time.monotonic()
    workroot=BASE/'work'
    workroot.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='p86_g2_',dir=workroot,ignore_cleanup_errors=True) as work:
        env.update(HOME=work,USERPROFILE=work,IPYTHONDIR=work)
        try:
            p=subprocess.run([str(py),'-X','utf8',str(test)],cwd=work,env=env,capture_output=True,text=True,encoding='utf8',errors='replace',timeout=120)
            output=p.stdout+'\n'+p.stderr
            status='PASS' if p.returncode==0 else ('FAIL' if 'AssertionError' in output else 'ERROR')
        except subprocess.TimeoutExpired as exc:
            status='TIMEOUT'; output=str(exc.stdout)+'\n'+str(exc.stderr)
        except OSError as exc:
            status='ENVIRONMENT_ERROR'; output=repr(exc)
    log=BASE/'logs'/('issue_'+number)/version/(variant+'.log')
    log.parent.mkdir(parents=True,exist_ok=True)
    log.write_text(output,encoding='utf8')
    errors=[s for s in output.splitlines() if re.match(r'^(?:\w*Error|AssertionError):',s)]
    result=dict(case='issue_'+number,variant=variant,version=version,status=status,detail='; '.join(errors)[-2000:],seconds=round(time.monotonic()-start,2),log=str(log),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),test_sha256=hashlib.sha256(test.read_bytes()).hexdigest())
    print(result['case'],variant,status,result['detail'][:200],flush=True)
    return result

if __name__=='__main__':
    import sys
    selected=sys.argv[1:] or CASES
    results=[]
    with ThreadPoolExecutor(max_workers=3) as executor:
        for future in as_completed([executor.submit(run,(n,v)) for n in selected for v in ['fixed','buggy']]):
            results.append(future.result())
            (BASE/'pilot_results.json').write_text(json.dumps(results,indent=2),encoding='utf8')
