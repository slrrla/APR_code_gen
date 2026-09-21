import concurrent.futures, hashlib, json, os, re, subprocess, tempfile, time
from pathlib import Path
BASE=Path(__file__).resolve().parent
ROOT=Path('C:/personal_webpage/my-portfolio/APR_code_gen/Part2_Create_test')
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
history=json.loads((ROOT/'test_validation/consolidated_runs.json').read_text(encoding='utf-8'))
cases=['issue_'+n for n in ['096','157','468','504','565','950','985']]
jobs=[r for r in history if r['case'] in cases]
assert len(jobs)==240
def run(r):
    r=dict(r)
    for k in ('subtests','seconds','batch'): r.pop(k,None)
    case=r['case']; variant=r['variant']; version=r['version']
    prefix=Path(r['command'][0]).parent
    source=BASE/'cases'/case/(variant+'.py'); test=source.with_name('test.py')
    env=os.environ.copy()
    env.update(MUT=str(source),PYTHONIOENCODING='utf-8',PYTHONDONTWRITEBYTECODE='1',OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',QISKIT_PARALLEL='FALSE',MPLBACKEND='Agg')
    if r.get('support_path'): env['PYTHONPATH']=r['support_path']
    env['PATH']=os.pathsep.join(map(str,[prefix,prefix/'Library/bin',prefix/'Scripts']))+os.pathsep+env['PATH']
    command=[str(prefix/'python.exe'),'-X','utf8',str(test),'-v']
    with tempfile.TemporaryDirectory(prefix='apr_repair_') as tmp:
        env.update(HOME=tmp,USERPROFILE=tmp,IPYTHONDIR=str(Path(tmp)/'.ipython'))
        check=subprocess.run([str(prefix/'python.exe'),'-c',"import importlib.metadata as m; print(m.version('qiskit'))"],env=env,cwd=tmp,capture_output=True,text=True,timeout=30)
        assert check.returncode==0 and check.stdout.strip()==version,(version,check.stdout,check.stderr)
        p=subprocess.run(command,env=env,cwd=tmp,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=180)
    log=p.stdout+'\n'+p.stderr
    path=BASE/'logs'/case/version/(variant+'.log'); path.parent.mkdir(parents=True,exist_ok=True); path.write_text(log,encoding='utf-8')
    count=re.search(r'Ran (\d+) tests?',log)
    status=('PASS' if count and int(count[1])>0 and 'skipped=' not in log else 'INVALID_RUN') if p.returncode==0 else ('FAIL' if 'AssertionError:' in log else 'ERROR')
    r.update(status=status,returncode=p.returncode,tests_run=int(count[1]) if count else 0,source=str(source),test=str(test),source_sha256=sha(source),test_sha256=sha(test),log=str(path),command=command,revision='repair01',detail='\n'.join(x for x in log.splitlines() if re.match(r'^(?:[\w.]*Error|AssertionError):',x)))
    print(case,version,variant,status,flush=True)
    return r
if __name__=='__main__':
    records=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        for f in concurrent.futures.as_completed([pool.submit(run,r) for r in jobs]):
            records.append(f.result())
            (BASE/'results.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
    print('COMPLETE',len(records),flush=True)
