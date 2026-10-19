"""Verify SE 61 across its selected Qiskit versions and controlled mutations."""
from concurrent.futures import ThreadPoolExecutor, as_completed
import contextlib
from datetime import datetime, timezone
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import unittest

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent
CASE = ROOT/'issue_061'
OBSERVER = ROOT/'bit_location_oracle.py'
TESTS = {'old': CASE/'test.py', 'permissive': BASE/'before'/'test_new.py', 'new': CASE/'test_new.py'}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def environment(version):
    prefix = ROOT.parent.parent/'Part1_Create_code'/'envs'/('qiskit_'+version.replace('.', '_'))
    env = os.environ.copy()
    for key in ('MUT', 'PYTHONPATH', 'PYTHONHOME'):
        env.pop(key, None)
    env.update(PYTHONDONTWRITEBYTECODE='1', PYTHONNOUSERSITE='1', PYTHONIOENCODING='utf-8',
               QISKIT_PARALLEL='FALSE', OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1')
    env['PATH'] = os.pathsep.join(map(str, [prefix, prefix/'Library/bin', prefix/'Scripts']))+os.pathsep+env['PATH']
    return prefix/'python.exe', env


def mutations():
    setup = '''from qiskit import QuantumCircuit, QuantumRegister
qr = QuantumRegister(2, 'q')
qc = QuantumCircuit(qr)
qc.h(0)
qc.cx(0, 1)
'''
    visit = 'for instruction, qargs, cargs in qc.data:\n    qbit = qargs[0]\n'
    locate = visit+'    location = qc.find_bit(qbit)\n'
    public = locate+'    print(location.index)\n    print(location.registers[0])\n'
    return {
        'fixed_control': ((CASE/'fixed.py').read_text(encoding='utf-8'), 'accept'),
        'luna_control': ((CASE/'fixed_luna.py').read_text(encoding='utf-8'), 'accept'),
        'original_buggy': ((CASE/'buggy.py').read_text(encoding='utf-8'), 'reject'),
        'grouped_public_control': (setup+locate+'    print(location.index, location.registers[0])\n', 'accept'),
        'formatted_string_control': (setup+locate+'    register, local = location.registers[0]\n    print(f"register={register}, local={local}, circuit={location.index}")\n', 'accept'),
        'register_local_only_control': (setup+locate+'    print(*location.registers[0])\n', 'accept'),
        'reversed_print_order_control': (setup+locate+'    print(location.registers[0])\n    print(location.index)\n', 'accept'),
        'reversed_instruction_reporting_control': (setup+public.replace('in qc.data:', 'in reversed(qc.data):'), 'accept'),
        'alternative_public_lookup_control': (setup+visit+'    register = next(reg for reg in qc.qregs if qbit in reg)\n    print(register)\n    print(list(register).index(qbit))\n', 'accept'),
        'custom_separator_control': (setup+locate+'    print(*location.registers[0], sep="::")\n', 'accept'),
        'equal_value_register_control': (setup+'equivalent = QuantumRegister(2, "q")\n'+locate+'    print(equivalent)\n    print(location.registers[0][1])\n', 'accept'),
        'wrong_index': (setup+locate+'    print(location.registers[0][0])\n    print(location.registers[0][1]+1)\n', 'reject'),
        'hardcoded_zero': (setup+visit+'    print(qr)\n    print(0)\n', 'reject'),
        'lookup_but_hardcoded_zero': (setup+locate+'    print(location.index*0)\n    print((location.registers[0][0], 0))\n', 'reject'),
        'equal_value_register_with_hardcoded_zero': (setup+'fake = QuantumRegister(2, "q")\n'+visit+'    print(0)\n    print((fake, 0))\n', 'reject'),
        'wrong_register': (setup+'fake = QuantumRegister(2, "wrong")\n'+visit+'    print(fake)\n    print(0)\n', 'reject'),
        'wrong_instruction_bit': (setup+public.replace('qargs[0]', 'qargs[-1]'), 'reject'),
        'same_first_bit_for_both_instructions': (setup+public.replace('qargs[0]', 'qc.data[0][1][0]'), 'reject'),
        'private_backreferences': (setup+visit+'    print(qbit._register)\n    print(qbit._index)\n', 'reject'),
        'private_backreferences_via_getattr': (setup+visit+'    print(getattr(qbit, "_register"))\n    print(getattr(qbit, "_index"))\n', 'reject'),
        'missing_cx': (setup.replace('qc.cx(0, 1)\n', '')+public, 'reject'),
        'changed_cx_wiring': (setup.replace('qc.cx(0, 1)', 'qc.cx(1, 0)')+public, 'reject'),
        'changed_operation_order': (setup.replace('qc.h(0)\nqc.cx(0, 1)', 'qc.cx(0, 1)\nqc.h(0)')+public, 'reject'),
        'circuit_index_reported_as_register_local': (setup+locate+'    print(location.registers[0][0])\n    print(location.index)\n', 'reject'),
        'only_one_instruction_reported': (setup+public+'    break\n', 'reject'),
    }


def load_test(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def execute(module, source, *, version, suite, variant, directory):
    module.MUT = str(source)
    stream = io.StringIO()
    started = time.monotonic()
    with contextlib.redirect_stdout(stream), contextlib.redirect_stderr(stream):
        outcome = unittest.TextTestRunner(stream=stream, verbosity=2).run(
            unittest.defaultTestLoader.loadTestsFromModule(module))
    assert outcome.testsRun == 1
    status = 'PASS' if outcome.wasSuccessful() else 'ERROR' if outcome.errors else 'FAIL'
    log = directory/(suite+'_'+variant+'.log')
    log.parent.mkdir(parents=True, exist_ok=True)
    log.write_text(stream.getvalue(), encoding='utf-8')
    detail_lines = [line.strip() for _, detail in outcome.errors+outcome.failures
                    for line in detail.splitlines() if 'Error:' in line]
    record = dict(case='issue_061', version=version, suite=suite, variant=variant,
                  status=status, tests_run=outcome.testsRun, failures=len(outcome.failures), errors=len(outcome.errors),
                  source=str(source), source_sha256=sha(source), test=str(TESTS[suite]), test_sha256=sha(TESTS[suite]),
                  observer_sha256=sha(OBSERVER) if suite=='new' else None,
                  detail='; '.join(dict.fromkeys(detail_lines)), log=str(log),
                  seconds=round(time.monotonic()-started,3), executed_at_utc=datetime.now(timezone.utc).isoformat())
    return record


def worker(version):
    import importlib.metadata as metadata
    import qiskit
    packages = dict(qiskit=metadata.version('qiskit'), core=qiskit.__version__,
                    python=sys.version.split()[0], interpreter=sys.executable)
    assert packages['qiskit'] == version
    records, audit = [], []
    for suite, test in TESTS.items():
        module = load_test(test, 'case61_'+suite)
        if suite != 'permissive':
            for variant in ('buggy', 'fixed', 'fixed_luna'):
                record = execute(module, CASE/(variant+'.py'), version=version, suite=suite, variant=variant,
                                 directory=CASE/'test_results_logs'/version)
                record['packages'] = packages
                records.append(record)
        for variant, (_, expectation) in mutations().items():
            record = execute(module, BASE/'mutants'/(variant+'.py'), version=version, suite=suite, variant=variant,
                             directory=BASE/'audit_logs'/version)
            record['expectation'] = expectation
            record['packages'] = packages
            audit.append(record)
    (BASE/'workers').mkdir(exist_ok=True)
    (BASE/'workers'/(version+'.json')).write_text(json.dumps(dict(records=records, audit=audit),indent=2),encoding='utf-8')
    print('VERIFIED', version, [(r['suite'],r['variant'],r['status']) for r in records], flush=True)


def main():
    selection=json.loads((ROOT.parent/'test_validation'/'batch01'/'selection.json').read_text(encoding='utf-8'))
    versions=next(case['versions'] for case in selection['cases'] if case['case']=='issue_061')
    assert len(versions)==15
    (BASE/'mutants').mkdir(exist_ok=True)
    for name,(source,_) in mutations().items():
        (BASE/'mutants'/(name+'.py')).write_text(source,encoding='utf-8')
    def run(version):
        python,env=environment(version)
        command=[str(python),'-X','utf8',str(Path(__file__).resolve()),'--worker',version]
        process=subprocess.run(command,env=env,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=180)
        (BASE/(version+'_worker.log')).write_text(process.stdout+'\n'+process.stderr,encoding='utf-8')
        assert process.returncode==0,(version,process.stdout,process.stderr)
        print(process.stdout.strip(),flush=True)
        return json.loads((BASE/'workers'/(version+'.json')).read_text(encoding='utf-8'))
    records,audit=[],[]
    with ThreadPoolExecutor(max_workers=4) as pool:
        for future in as_completed([pool.submit(run,version) for version in versions]):
            payload=future.result()
            records.extend(payload['records'])
            audit.extend(payload['audit'])
    assert len(records)==90 and len(audit)==len(mutations())*15*3
    for record in records+audit:
        assert sha(Path(record['source']))==record['source_sha256']
        assert sha(Path(record['test']))==record['test_sha256']
        if record['suite']=='new': assert sha(OBSERVER)==record['observer_sha256']
    (BASE/'results.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
    (CASE/'test_results_details.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
    (BASE/'audit_results.json').write_text(json.dumps(audit,indent=2),encoding='utf-8')
    summary=[]
    for mutation,(_,expectation) in mutations().items():
        row=dict(mutation=mutation,expectation=expectation)
        for suite in TESTS:
            matching=[r for r in audit if r['variant']==mutation and r['suite']==suite]
            assert len(matching)==15
            row[suite+'_pass']=sum(r['status']=='PASS' for r in matching)
        summary.append(row)
        print(row,flush=True)
    (BASE/'audit_summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    assert all(r['new_pass']==(15 if r['expectation']=='accept' else 0) for r in summary),summary
    assert all(r['status']==('ERROR' if r['variant']=='buggy' else 'PASS') for r in records if r['suite']=='new')
    print('COMPLETE:',len(records),'case executions and',len(audit),'mutation audit executions',flush=True)


if __name__=='__main__':
    if len(sys.argv)>1 and sys.argv[1]=='--worker': worker(sys.argv[2])
    else: main()
