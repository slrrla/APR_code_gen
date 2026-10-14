"""Audit old/new oracles with controlled mutations; never edit case sources."""
from concurrent.futures import ThreadPoolExecutor, as_completed
import contextlib
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import runpy
import subprocess
import sys
import unittest

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent
AUDIT = BASE/'oracle_audit'
CASES = {'issue_021_se': 'test-new.py', 'issue_058_se': 'test_new.py'}


def replace_once(source, before, after):
    assert source.count(before) == 1, (before, source.count(before))
    return source.replace(before, after, 1)


def mutations(case):
    fixed = (ROOT/case/'fixed.py').read_text(encoding='utf-8')
    luna = (ROOT/case/'fixed_luna.py').read_text(encoding='utf-8')
    is21 = case == 'issue_021_se'
    output = 'result' if is21 else 'v'
    expected = ('[1 / np.sqrt(2)] + [0]*6 + [1 / np.sqrt(2)]' if is21
                else '[-0.75] + [0.25]*7')
    expected_expr = 'np.array('+expected+', dtype=complex)'
    prefix = '\nimport numpy as np\n'
    append = lambda text: fixed + prefix + text + '\n'
    variants = {
        'fixed_control': (fixed, 'accept'),
        'luna_control': (luna, 'accept_new'),
        'original_buggy': ((ROOT/case/'buggy.py').read_text(encoding='utf-8'), 'reject'),
        'wrong_state': (append(output+' = np.array([1.] + [0.]*7)'), 'reject'),
        'wrong_dimension': (append(output+' = np.array([1., 0.])'), 'reject'),
        'unnormalized': (append(output+' = 2 * np.asarray('+output+')'), 'reject'),
        'wrong_relative_phase': (append(output+' = np.asarray('+output+').copy()\n'+output+'[-1] *= -1'), 'reject'),
        'global_phase_control': (append(output+' = 1j * np.asarray('+output+')'), 'accept'),
        'conflicting_wrong_statevector': (append('statevector = np.array([1.] + [0.]*7)'), 'reject'),
        'matching_array_alias_control': (append('statevector = np.asarray('+output+')'), 'accept'),
    }
    if is21:
        variants['wrong_gate_with_correct_state'] = (
            append('def cnotnot(gate_label="CNOTNOT"):\n    return QuantumCircuit(3).to_gate()'), 'reject')
        wrong_circuit = replace_once(fixed, 'circuit.append(cnotnot(), [q[0], q[1], q[2]])', 'circuit.x(1)')
        unsimulated = replace_once(fixed, 'result = execute(circuit, svsim).result().get_statevector()',
                                  'result = '+expected_expr)
        untranspiled = replace_once(luna, 'compiled_circuit = transpile(circuit, svsim)', 'compiled_circuit = circuit')
        authentic_format = replace_once(luna, 'statevector = np.asarray(result.get_statevector(compiled_circuit))',
                                        'statevector = np.asarray(result.get_statevector(compiled_circuit))\nresult = svsim.run(compiled_circuit)\ndel statevector')
        # Remove trailing print expressions that use the deliberately deleted alias.
        authentic_format = authentic_format[:authentic_format.index('print("a and b coefficients before simulation:')]
        failing = luna[:luna.index('result = svsim.run(compiled_circuit).result()')]
        failing = replace_once(failing, 'compiled_circuit = transpile(circuit, svsim)', 'compiled_circuit = circuit')
        failing += prefix + 'try:\n    result = svsim.run(compiled_circuit).result().get_statevector()\nexcept Exception:\n    result = '+expected_expr+'\nstatevector = result\n'
        state_only = replace_once(luna, 'statevector = np.asarray(result.get_statevector(compiled_circuit))',
                                  'statevector = np.asarray(result.get_statevector(compiled_circuit))\ndel result')
        extra_wrong_job = append('unrelated = QuantumCircuit(3)\nsvsim.run(unrelated).result()')
    else:
        variants['wrong_gate_with_correct_state'] = (
            append('def diffuser(nqubits):\n    return QuantumCircuit(nqubits).to_gate()'), 'reject')
        variants['wrong_four_qubit_gate_only'] = (
            append('original_diffuser = diffuser\ndef diffuser(nqubits):\n    return QuantumCircuit(nqubits).to_gate() if nqubits == 4 else original_diffuser(nqubits)'), 'reject')
        wrong_circuit = replace_once(fixed, 'circuit.append(diffuser(3), psi)', 'circuit.x(0)')
        unsimulated = replace_once(fixed, 'job = backend.run(circuit)', '# simulator execution removed')
        unsimulated = replace_once(unsimulated, 'v = job.result().get_statevector(circuit)',
                                  'import numpy as np\nv = '+expected_expr)
        untranspiled = replace_once(luna, 'compiled_circuit = transpile(circuit, backend)', 'compiled_circuit = circuit')
        authentic_format = luna[:luna.index('statevector = job.result().get_statevector(compiled_circuit)')]
        failing = luna[:luna.index('job = backend.run(compiled_circuit)')]
        failing = replace_once(failing, 'compiled_circuit = transpile(circuit, backend)', 'compiled_circuit = circuit')
        failing += prefix + 'try:\n    v = backend.run(compiled_circuit).result().get_statevector()\nexcept Exception:\n    v = '+expected_expr+'\nstatevector = v\n'
        state_only = replace_once(luna, 'statevector = job.result().get_statevector(compiled_circuit)',
                                  'statevector = job.result().get_statevector(compiled_circuit)\ndel job')
        extra_wrong_job = append('unrelated = QuantumCircuit(3)\nbackend.run(unrelated).result()')
    variants.update({
        'wrong_circuit_hidden_by_correct_statevector': (wrong_circuit+prefix+'statevector = '+expected_expr+'\n', 'reject'),
        'hardcoded_output_without_simulator': (unsimulated, 'reject'),
        'untranspiled_luna': (untranspiled, 'reject'),
        'genuine_job_output_control': (authentic_format, 'accept_new'),
        'failed_simulation_exception_masked_by_hardcode': (failing, 'reject'),
        'genuine_statevector_only_control': (state_only, 'accept_new'),
        'extra_wrong_simulation_with_correct_export': (extra_wrong_job, 'reject'),
    })
    return variants


def worker(version):
    import numpy as np
    from qiskit.quantum_info import Statevector
    records = []
    bindings = []
    for case, new_test in CASES.items():
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream), contextlib.redirect_stderr(stream):
            namespace = runpy.run_path(str(ROOT/case/'fixed_luna.py'))
        result = namespace['result'] if case == 'issue_021_se' else namespace['job'].result()
        actual_backend_state = Statevector(result.get_statevector(namespace['compiled_circuit']))
        exported_state = Statevector(namespace['statevector'])
        expected = ([1/np.sqrt(2)] + [0]*6 + [1/np.sqrt(2)] if case == 'issue_021_se'
                    else [-0.75] + [0.25]*7)
        assert result.success
        np.testing.assert_allclose(actual_backend_state.data, exported_state.data, atol=1e-12, rtol=0)
        assert actual_backend_state.is_valid() and actual_backend_state.equiv(Statevector(expected))
        bindings.append(dict(case=case, version=version, backend_success=bool(result.success),
                             exported_state_matches_backend=True, backend_state_matches_original_intent=True,
                             source_sha256=hashlib.sha256((ROOT/case/'fixed_luna.py').read_bytes()).hexdigest()))
        for suite, filename in [('old', 'test.py'), ('new', new_test)]:
            spec = importlib.util.spec_from_file_location('oracle_'+case+'_'+suite, ROOT/case/filename)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            for name, (_, expectation) in mutations(case).items():
                source = AUDIT/'mutants'/case/(name+'.py')
                module.MUT = str(source)
                stream = io.StringIO()
                with contextlib.redirect_stdout(stream), contextlib.redirect_stderr(stream):
                    outcome = unittest.TextTestRunner(stream=stream, verbosity=2).run(
                        unittest.defaultTestLoader.loadTestsFromModule(module))
                assert outcome.testsRun == 1
                status = 'PASS' if outcome.wasSuccessful() else 'FAIL' if outcome.failures else 'ERROR'
                log = AUDIT/'logs'/version/case/(suite+'_'+name+'.log')
                log.parent.mkdir(parents=True, exist_ok=True)
                log.write_text(stream.getvalue(), encoding='utf-8')
                records.append(dict(case=case, version=version, suite=suite, mutation=name,
                                    expectation=expectation, status=status, tests_run=outcome.testsRun,
                                    source=str(source), source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                                    test=str(ROOT/case/filename),
                                    test_sha256=hashlib.sha256((ROOT/case/filename).read_bytes()).hexdigest(),
                                    observer_sha256=hashlib.sha256((ROOT/'simulation_oracle.py').read_bytes()).hexdigest() if suite=='new' else None,
                                    log=str(log), errors=[detail for _, detail in outcome.errors+outcome.failures]))
    (AUDIT/(version+'.json')).write_text(json.dumps(records, indent=2), encoding='utf-8')
    (AUDIT/(version+'_luna_binding.json')).write_text(json.dumps(bindings, indent=2), encoding='utf-8')
    print('AUDITED', version, len(records), flush=True)


def main():
    from run_matrix import environment
    AUDIT.mkdir(exist_ok=True)
    for case in CASES:
        target = AUDIT/'mutants'/case
        target.mkdir(parents=True, exist_ok=True)
        for name, (source, _) in mutations(case).items():
            (target/(name+'.py')).write_text(source, encoding='utf-8')
    probes = json.loads((BASE/'environments.json').read_text(encoding='utf-8'))
    def run(version):
        python, env = environment(version)
        process = subprocess.run([str(python), '-X', 'utf8', str(Path(__file__).resolve()), '--worker', version],
                                 env=env, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=180)
        (AUDIT/(version+'_worker.log')).write_text(process.stdout+'\n'+process.stderr, encoding='utf-8')
        assert process.returncode == 0, (version, process.stdout, process.stderr)
        print(process.stdout.strip(), flush=True)
        return json.loads((AUDIT/(version+'.json')).read_text(encoding='utf-8'))
    records = []
    with ThreadPoolExecutor(max_workers=4) as pool:
        for future in as_completed([pool.submit(run, v) for v in probes]):
            records.extend(future.result())
    (AUDIT/'results.json').write_text(json.dumps(records, indent=2), encoding='utf-8')
    summary = []
    for case in CASES:
        for name, (_, expectation) in mutations(case).items():
            item = dict(case=case, mutation=name, expectation=expectation)
            for suite in ('old', 'new'):
                matching = [r for r in records if r['case']==case and r['mutation']==name and r['suite']==suite]
                assert len(matching) == len(probes)
                item[suite+'_pass'] = sum(r['status']=='PASS' for r in matching)
                item[suite+'_total'] = len(matching)
            expected_passes = 0 if expectation == 'reject' else len(probes)
            assert item['new_pass'] == expected_passes, item
            summary.append(item)
            print(item, flush=True)
    (AUDIT/'summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
    bindings = [item for version in probes
                for item in json.loads((AUDIT/(version+'_luna_binding.json')).read_text(encoding='utf-8'))]
    assert len(bindings) == 24
    (AUDIT/'luna_simulation_evidence.json').write_text(json.dumps(bindings, indent=2), encoding='utf-8')
    findings = dict(status='HARDENED_ORACLE_CHECKS_PASSED', oracle_executions=len(records),
                    qiskit_versions=list(probes),
                    closed_gaps=['wrong circuit hidden by a preferred exported statevector',
                                 'hardcoded output without backend execution',
                                 'simulator failure masked by a replacement output'],
                    normal_output_formats_and_global_phase_preserved=True,
                    observer_sha256=hashlib.sha256((ROOT/'simulation_oracle.py').read_bytes()).hexdigest(),
                    scope='Real local Aer backend execution is required for these single-purpose examples. Every observed experiment and exported simulation output must match. This is not a security sandbox against a program that deliberately modifies the test process.')
    (AUDIT/'findings.json').write_text(json.dumps(findings, indent=2), encoding='utf-8')
    print('VERIFIED', len(bindings), 'independent Luna backend/output bindings', flush=True)
    print('VERIFIED', len(records), 'oracle audit executions', flush=True)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--worker':
        worker(sys.argv[2])
    else:
        main()
