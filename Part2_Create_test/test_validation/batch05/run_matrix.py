"""Run each standalone test.py against both MUTs in its listed Qiskit versions.

No target source rewriting or exception swallowing. Every subprocess has an
isolated cwd and home. Raw stdout/stderr, versions and SHA256s are retained.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import time

BASE = Path(__file__).resolve().parent
SUPPORT_ROOT = Path('C:/Users/haha9/.codex/visualizations/2026/09/07/01a07c80-3ea3-71b3-9c09-5b72170c3cdf/quantum_apr_batch05/support')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def run_one(job):
    case, version, variant, probe, test_root = job
    name = case['case']
    test = test_root/name/'test.py'
    source = Path(case['source_dir'])/(variant+'.py')
    prefix = Path(probe['interpreter']).parent
    env = os.environ.copy()
    env.update(MUT=str(source), PYTHONIOENCODING='utf-8', PYTHONDONTWRITEBYTECODE='1',
               OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1',
               QISKIT_PARALLEL='FALSE', MPLBACKEND='Agg')
    env['PATH'] = os.pathsep.join(map(str,[prefix,prefix/'Library/bin',prefix/'Scripts']))+os.pathsep+env['PATH']
    # Supplement non-Qiskit dependencies without modifying shared environments.
    support = None
    if name == 'issue_742':
        tag = 'py' + ''.join(probe['python'].split('.')[:2])
        support = SUPPORT_ROOT/tag
        if not support.is_dir(): raise RuntimeError('Missing support dependencies: '+str(support))
        env['PYTHONPATH'] = str(support)
    record = {'case':name,'version':version,'variant':variant,'source':str(source),
              'test':str(test),'source_sha256':sha(source),'test_sha256':sha(test),
              'python':probe.get('python'),'qiskit':probe.get('qiskit'),
              'terra':probe.get('qiskit-terra'),'aer':probe.get('qiskit-aer'),
              'numpy':probe.get('numpy'),'ipython':probe.get('ipython')}
    record['support_path'] = str(support) if support else None
    if support:
        record['runtime'] = '0.30.0' if version.startswith('1.') else '0.40.1'
        record['psutil'] = '7.2.2'
    command = [probe['interpreter'],'-X','utf8',str(test),'-v']
    record['command']=command
    started = time.monotonic()
    timeout = 300 if name == 'issue_742' else 120
    output=''
    with tempfile.TemporaryDirectory(prefix='apr_run_') as work:
        env.update(USERPROFILE=work, HOME=work, IPYTHONDIR=str(Path(work)/'.ipython'))
        try:
            p = subprocess.run(command,cwd=work,env=env,capture_output=True,text=True,
                               encoding='utf-8',errors='replace',timeout=timeout)
            output=p.stdout+'\n'+p.stderr
            record['returncode']=p.returncode
            if p.returncode == 0:
                record['status']='PASS' if re.search(r'Ran [1-9]\d* tests?', output) and not re.search(r'skipped=\d',output) else 'INVALID_RUN'
            elif 'AssertionError:' in output:
                record['status']='FAIL'
            else:
                record['status']='ERROR'
            record['tests_run']=int(re.search(r'Ran (\d+) tests?',output).group(1)) if re.search(r'Ran (\d+) tests?',output) else 0
            errors=[line.strip() for line in output.splitlines() if re.match(r'^(?:[\w.]*Error|AssertionError|unittest.case.SkipTest):',line)]
            record['detail']='; '.join(dict.fromkeys(errors))[:2000]
        except subprocess.TimeoutExpired as e:
            record.update(status='TIMEOUT',returncode=None,tests_run=None,detail=str(timeout)+' second execution timeout')
            output=str(e.stdout or '')+'\n'+str(e.stderr or '')
        except Exception as e:
            record.update(status='ENVIRONMENT_ERROR',returncode=None,tests_run=0,detail=repr(e))
    record['seconds']=round(time.monotonic()-started,3)
    log=BASE/'logs'/name/version/(variant+'.log')
    log.parent.mkdir(parents=True,exist_ok=True)
    log.write_text(output,encoding='utf-8')
    record['log']=str(log)
    print(name,version,variant,record['status'],record['detail'][:160],flush=True)
    return record

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--pilot',action='store_true')
    parser.add_argument('--cases',nargs='*')
    parser.add_argument('--versions',nargs='*')
    parser.add_argument('--workers',type=int,default=4)
    parser.add_argument('--test-root',type=Path,default=BASE/'tests')
    args=parser.parse_args()
    selection=json.loads((BASE/'selection.json').read_text(encoding='utf-8'))
    probes=json.loads((BASE/'environments.json').read_text(encoding='utf-8'))
    jobs=[]
    for case in selection['cases']:
        if args.cases and case['case'] not in args.cases: continue
        versions=[case['versions'][0]] if args.pilot else case['versions']
        for version in versions:
            if args.versions and version not in args.versions: continue
            if not probes[version]['ok']: raise RuntimeError('Exact environment failed probe: '+version)
            for variant in ['buggy','fixed']:
                jobs.append((case,version,variant,probes[version],args.test_root.resolve()))
    path=BASE/('pilot_results.json' if args.pilot else 'results.json')
    results=json.loads(path.read_text(encoding='utf-8')) if (args.cases or args.versions) and path.exists() else []
    keys={(case['case'],version,variant) for case,version,variant,_,_ in jobs}
    results=[r for r in results if (r['case'],r['version'],r['variant']) not in keys]
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        for future in as_completed([pool.submit(run_one,job) for job in jobs]):
            results.append(future.result())
            path.write_text(json.dumps(results,indent=2),encoding='utf-8')
    print('FINISHED',len(jobs),'executions',flush=True)
