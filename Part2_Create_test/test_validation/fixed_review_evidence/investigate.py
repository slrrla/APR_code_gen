"""Read-only analysis and isolated reruns. No dataset sources or tests are edited."""
import contextlib, hashlib, io, json, os, re, runpy, subprocess, sys, tempfile
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
BASE=Path(__file__).resolve().parent
ROOT=Path('C:/personal_webpage/my-portfolio/APR_code_gen/Part2_Create_test')
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def probe(case):
    import numpy as np
    from qiskit.quantum_info import Operator
    with contextlib.redirect_stdout(io.StringIO()):
        m=runpy.run_path(str(ROOT/'reconstructed_cases'/case/'test.py'))
        if case=='issue_468':
            a,b,c=m['captured_commutator']()
            out={k:np.asarray(m['matrix'](v)).real.tolist() for k,v in [('a',a),('b',b),('commutator',c)]}
        else:
            fn=m.get('target') or m.get('load_target')
            ns=fn()
            if case=='issue_157': out={'controls':ns['controlled_gate'].num_ctrl_qubits,'qubits':ns['controlled_gate'].num_qubits}
            elif case=='issue_504':
                from qiskit import QuantumCircuit,QuantumRegister
                out={}
                for label in ['000','101','111']:
                    qr=QuantumRegister(3);qc=QuantumCircuit(qr)
                    ns['oracle'](qc,qr,label)
                    out[label]=[format(i,'03b') for i,v in enumerate(np.diag(Operator(qc).data)) if abs(v+1)<1e-10]
            elif case=='issue_565':
                import itertools
                matrix=np.asarray(ns['mixer_op'].to_matrix())
                tours=[sum(1<<(3*t+c) for t,c in enumerate(p)) for p in itertools.permutations(range(3))]
                # Independent four-qubit Pauli expansion: labels in local order a,b,c,d.
                I=np.eye(2);X=np.array([[0,1],[1,0]]);Y=np.array([[0,-1j],[1j,0]])
                def term(ys):
                    result=np.array([[1.]])
                    for q in reversed(range(4)): result=np.kron(result,Y if q in ys else X)
                    return result
                def expansion(negative):
                    return 2*(term([])+term([0,1,2,3])+sum((-1 if pair in negative else 1)*term(pair) for pair in itertools.combinations(range(4),2)))
                current=expansion({(0,1),(2,3)})
                reference=expansion({(0,3),(1,2)})
                out={'tour_indices':tours,'tour_column_norms':[float(np.linalg.norm(matrix[:,t])) for t in tours],
                     'local_swap_1001_to_0110_actual':float(current[6,9].real),
                     'local_swap_1001_to_0110_reference':float(reference[6,9].real),
                     'local_wrong_move_0011_to_1100_actual':float(current[12,3].real)}
            elif case=='issue_950':
                diag=np.diag(ns['op'].data)
                out={'label':ns['label'],'single_excitation_phases':[float(diag[1<<q].real) for q in range(10)]}
            elif case=='issue_985':
                actual=Operator(ns['transpiled']).data;expected=np.diag([1,np.exp(.5j)])
                out={'max_error':float(abs(actual-expected).max()),'phase_restored_error':float(abs(np.exp(.25j)*actual-expected).max()),
                     'actual_determinant':str(np.linalg.det(actual)),'expected_determinant':str(np.linalg.det(expected))}
    print('PROBE_JSON '+json.dumps(out))
if len(sys.argv)>1:
    probe(sys.argv[1]);sys.exit()
runs=json.loads((ROOT/'test_validation/consolidated_runs.json').read_text(encoding='utf-8'))
data=json.loads((ROOT/'test_validation/consolidated_data.json').read_text(encoding='utf-8'))
cases=sorted({p['case'] for p in data['pairs'] if p['fixed']=='FAIL'})
assert len(cases)==7
selected=[]; historical=[]
for case in cases:
    rows=sorted([r for r in runs if r['case']==case and r['variant']=='fixed'],key=lambda r:tuple(map(int,r['version'].split('.'))))
    assert all(r['status']=='FAIL' for r in rows)
    for r in rows:
        assert sha(r['source'])==r['source_sha256']
        assert sha(ROOT/'reconstructed_cases'/case/'test.py')==r['test_sha256']
        log=Path(r['log']).read_text(encoding='utf-8')
        assert 'FAILED (failures=1)' in log
        historical.append(r)
    selected.extend([rows[0],rows[-1]])
def rerun(r,diagnostic=False):
    env=os.environ.copy();prefix=Path(r['command'][0]).parent
    env.update(MUT=r['source'],PYTHONIOENCODING='utf-8',PYTHONDONTWRITEBYTECODE='1',
        OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',QISKIT_PARALLEL='FALSE',MPLBACKEND='Agg')
    if r.get('support_path'):env['PYTHONPATH']=r['support_path']
    env['PATH']=os.pathsep.join(map(str,[prefix,prefix/'Library/bin',prefix/'Scripts']))+os.pathsep+env['PATH']
    cmd=[r['command'][0],'-X','utf8',str(BASE/'investigate.py'),r['case']] if diagnostic else [r['command'][0],'-X','utf8',str(ROOT/'reconstructed_cases'/r['case']/'test.py'),'-v']
    with tempfile.TemporaryDirectory(prefix='apr_review_') as tmp:
        env.update(HOME=tmp,USERPROFILE=tmp,IPYTHONDIR=str(Path(tmp)/'.ipython'))
        p=subprocess.run(cmd,env=env,cwd=tmp,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=180)
    log=p.stdout+'\n'+p.stderr
    path=BASE/'logs'/(r['case']+'_'+r['version']+('_probe' if diagnostic else '_rerun')+'.log')
    path.parent.mkdir(exist_ok=True)
    path.write_text(log,encoding='utf-8')
    if diagnostic:
        assert p.returncode==0,log
        result=json.loads(next(l[11:] for l in log.splitlines() if l.startswith('PROBE_JSON ')))
    else:
        assert p.returncode==1 and 'FAILED (failures=1)' in log,log
        result={'status':'FAIL','tests_run':int(re.search(r'Ran (\d+) tests?',log).group(1))}
    print(r['case'],r['version'],'PROBE' if diagnostic else 'REPRODUCED',flush=True)
    return dict(case=r['case'],version=r['version'],result=result,log=str(path))
with ThreadPoolExecutor(max_workers=3) as pool:
    fresh=list(pool.map(rerun,selected))
probes=[rerun(r,True) for r in selected[::2] if r['case']!='issue_096']
payload={'historical':historical,'reruns':fresh,'probes':probes,'original_workbook_sha256':sha(ROOT/'test_validation/Quantum_APR_Validation.xlsx')}
(BASE/'evidence.json').write_text(json.dumps(payload,indent=2),encoding='utf-8')
print('VERIFIED 120 historical failure records and 14 new representative reruns. Six independent diagnostic probes completed.')
