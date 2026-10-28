"""Write the group-2 standalone intent oracles; never edit a target source."""
from pathlib import Path
import textwrap

ROOT = Path(__file__).resolve().parents[2]
HEADER = '''import contextlib
import io
import os
import random
import runpy
import unittest
from unittest.mock import patch

CASE_DIR = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("MUT", os.path.join(CASE_DIR, "fixed.py"))


def load_target():
    """Run the original script; seed sampling, but do not alter its logic."""
    import numpy as np
    import qiskit
    random.seed(7301)
    np.random.seed(7301)
    try:
        from qiskit.aqua import aqua_globals
        aqua_globals.random_seed = 7301
    except ImportError:
        pass
    try:
        from qiskit.utils import algorithm_globals
        algorithm_globals.random_seed = 7301
    except ImportError:
        pass
    output = io.StringIO()
    original_execute = getattr(qiskit, "execute", None)
    def seeded_execute(*args, **kwargs):
        kwargs.setdefault("seed_simulator", 7301)
        kwargs.setdefault("seed_transpiler", 7301)
        return original_execute(*args, **kwargs)
    with contextlib.ExitStack() as stack:
        stack.enter_context(contextlib.redirect_stdout(output))
        if original_execute is not None:
            stack.enter_context(patch.object(qiskit, "execute", seeded_execute))
        namespace = runpy.run_path(MUT)
    return namespace, output.getvalue()


def circuits(namespace):
    from qiskit import QuantumCircuit
    return [value for value in namespace.values() if isinstance(value, QuantumCircuit)]


'''
FOOTER = '''

if __name__ == "__main__":
    unittest.main(argv=[""])
'''
TESTS = {}

TESTS['139'] = ("Measure only qubit 5 and return one-bit measurement strings.", '''
class Test(unittest.TestCase):
    def test_single_bit_measurement(self):
        ns, _ = load_target()
        qc = circuits(ns)[-1]
        self.assertEqual(qc.num_qubits, 9)
        self.assertEqual(qc.num_clbits, 1)
        measured = [item for item in qc.data if item[0].name == 'measure']
        self.assertEqual(len(measured), 1)
        self.assertEqual(qc.qubits.index(measured[0][1][0]), 5)
        self.assertEqual(qc.clbits.index(measured[0][2][0]), 0)
        counts = ns['result'].get_counts()
        self.assertTrue(counts)
        self.assertTrue(set(counts).issubset({'0', '1'}))
        self.assertEqual(sum(counts.values()), 1000)
''')
TESTS['147'] = ("Actually solve min(5*x1-7*x2), whose unique optimum is (0,1).", '''
class Test(unittest.TestCase):
    def test_binary_optimum_is_returned(self):
        import numpy as np
        ns, _ = load_target()
        results = [value for value in ns.values()
                   if hasattr(value, 'x') and hasattr(value, 'fval')]
        self.assertTrue(results, 'The program must return an optimization result.')
        result = results[-1]
        np.testing.assert_allclose(result.x, [0, 1], atol=1e-9)
        self.assertAlmostEqual(result.fval, -7, places=7)
''')
TESTS['151'] = ("Submit all ten Grover circuits together to avoid ten backend queue waits.", '''
class Test(unittest.TestCase):
    def test_one_backend_submission_for_ten_experiments(self):
        from qiskit import BasicAer
        backend_type = type(BasicAer.get_backend('qasm_simulator'))
        original_run = backend_type.run
        executions = []
        def observe(backend, *args, **kwargs):
            payload = args[0] if args else kwargs.get('qobj', kwargs.get('run_input'))
            count = len(payload.experiments) if hasattr(payload, 'experiments') else (len(payload) if isinstance(payload, (list, tuple)) else 1)
            job = original_run(backend, *args, **kwargs)
            executions.append((count, job))
            return job
        with patch.object(backend_type, 'run', observe):
            load_target()
        self.assertEqual([count for count, _ in executions], [10])
        result = executions[0][1].result()
        self.assertTrue(result.success)
        self.assertEqual(len(result.results), 10)
        # construct_circuit intentionally returns unmeasured circuits. The
        # batching task does not require a particular classical readout format.
''')
TESTS['152'] = ("Match the negative-exponent, normalized four-point Fourier transform.", '''
class Test(unittest.TestCase):
    def test_dft_phase_convention(self):
        import numpy as np
        ns, _ = load_target()
        expected = .5 * np.array([[1,1,1,1], [1,-1j,-1,1j], [1,-1,1,-1], [1,1j,-1,-1j]])
        np.testing.assert_allclose(ns['qft_matrix'], expected, atol=1e-9)
''')
TESTS['162'] = ("Execute a Bell circuit on BasicAer without unsupported Aer method options.", '''
class Test(unittest.TestCase):
    def test_supported_backend_configuration(self):
        import qiskit
        original_execute = qiskit.execute
        unsupported = []
        def observe(circuit, backend, *args, **kwargs):
            options = kwargs.get('backend_options', {})
            module = type(backend).__module__
            if 'basicaer' in module and 'method' in options:
                unsupported.append(options['method'])
            return original_execute(circuit, backend, *args, **kwargs)
        with patch.object(qiskit, 'execute', observe):
            ns, _ = load_target()
        self.assertFalse(unsupported, 'BasicAer does not implement Aer simulation-method selection.')
        self.assertTrue(ns['result'].success)
        self.assertEqual(set(ns['result'].get_counts()), {'00', '11'})
''')
TESTS['163'] = ("Swap only |01> and |10>, preserving |00>, |11>, and coherence.", '''
class Test(unittest.TestCase):
    def test_complete_two_level_operator(self):
        import numpy as np
        from qiskit.quantum_info import Operator
        ns, _ = load_target()
        qc = circuits(ns)[-1].copy()
        # The preparation fixes equal coefficients and masks incorrect permutations.
        # Test the exported operation on the complete basis, excluding preparation.
        qc.data = [item for item in qc.data if item[0].name != 'initialize']
        expected = np.array([[1,0,0,0], [0,0,1,0], [0,1,0,0], [0,0,0,1]])
        self.assertTrue(Operator(qc).equiv(Operator(expected)),
                        'The transformation must act only on the requested two-level subspace.')
''')
TESTS['165'] = ("Run the migrated VQE and return a finite low-energy solution of the Hamiltonian.", '''
class Test(unittest.TestCase):
    def test_migrated_vqe_result(self):
        import numpy as np
        ns, _ = load_target()
        candidates = [value for value in ns.values() if hasattr(value, 'eigenvalue')]
        self.assertTrue(candidates, 'A VQE computation result is required.')
        energy = complex(candidates[-1].eigenvalue)
        exact = np.linalg.eigvalsh(np.array(ns['Hamiltonian']))[0]
        self.assertAlmostEqual(energy.imag, 0, places=7)
        self.assertTrue(np.isfinite(energy.real))
        self.assertLess(abs(energy.real - exact), .5)
''')
TESTS['171'] = ("Average Pauli-channel fidelity is 1-2*(px+py+pz)/3.", '''
class Test(unittest.TestCase):
    def test_average_fidelity(self):
        ns, _ = load_target()
        function = ns['average_fidelity']
        for probabilities, expected in [((0,0,0),1), ((.02,.03,.05),14/15), ((1,0,0),1/3), ((0,.3,.3),.6)]:
            with self.subTest(probabilities=probabilities):
                self.assertAlmostEqual(function(*probabilities), expected, places=12)
''')
TESTS['191'] = ("Recover theta=pi/3 through phase-sensitive X and Y tomography.", '''
class Test(unittest.TestCase):
    def test_phase_estimate_and_measurement_information(self):
        import math
        from qiskit.quantum_info import Statevector
        ns, _ = load_target()
        estimates = [ns[key] for key in ('estimated_theta', 'theta_estimate') if key in ns]
        self.assertTrue(estimates, 'Return the phase estimate rather than only Z-basis counts.')
        self.assertAlmostEqual(float(estimates[-1]), math.pi/3, delta=.08)
        probabilities = []
        for qc in circuits(ns):
            probabilities.append(Statevector.from_instruction(qc.remove_final_measurements(inplace=False)).probabilities()[0])
        self.assertTrue(any(abs(p-.75)<1e-9 for p in probabilities), 'X measurement must reveal cos(theta).')
        self.assertTrue(any(abs(p-(2+math.sqrt(3))/4)<1e-9 for p in probabilities), 'Y measurement must reveal sin(theta).')
''')
TESTS['199'] = ("Place the two CNOT layers on their intended little-endian tensor factors.", '''
class Test(unittest.TestCase):
    def test_concrete_eight_basis_mapping(self):
        import numpy as np
        ns, _ = load_target()
        actual = np.matmul(ns['layer2'], ns['layer1'])
        # Column j is the output for input basis state |j> (from the source question).
        expected = np.eye(8)[:, [0,7,6,1,4,3,2,5]]
        np.testing.assert_allclose(actual, expected, atol=1e-12)
''')
TESTS['201'] = ("QPE with theta=1/3 has the correctly ordered inverse-QFT distribution.", '''
class Test(unittest.TestCase):
    def test_exact_phase_distribution(self):
        import numpy as np
        from qiskit.quantum_info import Statevector
        ns, _ = load_target()
        qc = circuits(ns)[-1].remove_final_measurements(inplace=False)
        probabilities = Statevector.from_instruction(qc).probabilities(qargs=[0,1,2])
        expected = np.array([abs(sum(np.exp(2j*np.pi*k*(1/3-y/8)) for k in range(8))/8)**2 for y in range(8)])
        np.testing.assert_allclose(probabilities, expected, atol=1e-10)
        # theta=1/3 happens to mask reversal of the three counting qubits.
        # Exercise the exported inverse-QFT on the complete computational basis.
        from qiskit import QuantumCircuit
        from qiskit.quantum_info import Operator
        inverse = QuantumCircuit(3)
        ns['qft_dagger'](inverse, 3)
        fourier = np.array([[np.exp(-2j*np.pi*j*k/8)/np.sqrt(8) for k in range(8)] for j in range(8)])
        self.assertTrue(Operator(inverse).equiv(Operator(fourier)))
''')
TESTS['221'] = ("Expose ordered H/CX instruction data programmatically, without a printing error.", '''
class Test(unittest.TestCase):
    def test_instruction_data_output(self):
        import builtins
        printed = []
        original_print = builtins.print
        def observe(*args, **kwargs):
            printed.extend(args)
            return original_print(*args, **kwargs)
        with patch.object(builtins, 'print', observe):
            load_target()
        sequences = []
        for value in printed:
            if isinstance(value, (str, bytes)) or hasattr(value, 'num_qubits'):
                continue
            try:
                sequences.append([getattr(item[0], 'name', '') for item in value])
            except (TypeError, IndexError, KeyError):
                pass
        self.assertIn(['h', 'cx'], sequences)
''')
TESTS['271'] = ("Display the ancilla as the rightmost bit in the requested MCX distribution.", '''
class Test(unittest.TestCase):
    def test_requested_output_bit_order(self):
        ns, _ = load_target()
        counts = ns['job'].result().get_counts()
        self.assertEqual(set(counts), {'0000','0010','0100','0110','1000','1010','1100','1111'})
        self.assertEqual(sum(counts.values()), 1000)
''')
TESTS['275'] = ("Represent the given matrix by zero-padding, preserving its spectrum.", '''
class Test(unittest.TestCase):
    def test_matrix_operator_preserves_original_matrix(self):
        import numpy as np
        original_eig = np.linalg.eig
        inputs = []
        def observe(matrix, *args, **kwargs):
            inputs.append(np.array(matrix, copy=True))
            return original_eig(matrix, *args, **kwargs)
        with patch.object(np.linalg, 'eig', observe):
            ns, _ = load_target()
        self.assertTrue(inputs, 'The original matrix must be retained for spectral comparison.')
        original = inputs[0]
        expected = np.zeros((4,4), dtype=complex)
        expected[:3,:3] = original
        from qiskit.aqua.operators import WeightedPauliOperator, op_converter
        representations = []
        for value in ns.values():
            if isinstance(value, WeightedPauliOperator):
                matrix = op_converter.to_matrix_operator(value).matrix
                representations.append(matrix.toarray() if hasattr(matrix, 'toarray') else np.asarray(matrix))
        self.assertTrue(any(matrix.shape == (4,4) and np.allclose(matrix, expected, atol=1e-9)
                            for matrix in representations),
                        'A plain three-dimensional matrix must not become an eight-dimensional fermionic operator.')
''')
TESTS['316'] = ("A controlled T with zero control leaves |0+> unchanged.", '''
class Test(unittest.TestCase):
    def test_controlled_phase(self):
        import math
        from qiskit.quantum_info import Statevector
        ns, _ = load_target()
        state = Statevector.from_instruction(circuits(ns)[-1])
        self.assertTrue(state.equiv(Statevector([1/math.sqrt(2),0,1/math.sqrt(2),0])))
''')
TESTS['334'] = ("X+iY is the raising operator [[0,2],[0,0]].", '''
class Test(unittest.TestCase):
    def test_complex_pauli_coefficient(self):
        import numpy as np
        ns, _ = load_target()
        np.testing.assert_allclose(ns['result'], [[0,2],[0,0]], atol=1e-12)
''')
TESTS['346'] = ("The demonstrated rotation has RZ(theta)'s full action, up to global phase.", '''
class Test(unittest.TestCase):
    def test_z_rotation_operator(self):
        import numpy as np
        from qiskit.quantum_info import Operator
        ns, _ = load_target()
        expected = Operator(np.diag([np.exp(-.5j*ns['theta']), np.exp(.5j*ns['theta'])]))
        self.assertTrue(Operator(circuits(ns)[-1]).equiv(expected))
''')
TESTS['347'] = ("Evaluate ten expectation values with one batched backend submission.", '''
class Test(unittest.TestCase):
    def test_batched_expectations(self):
        import numpy as np
        try:
            from qiskit_aer.backends.aerbackend import AerBackend
        except ImportError:
            from qiskit.providers.aer.backends.aerbackend import AerBackend
        original_run = AerBackend.run
        jobs = []
        def observe(backend, *args, **kwargs):
            job = original_run(backend, *args, **kwargs)
            jobs.append(job)
            return job
        with patch.object(AerBackend, 'run', observe):
            ns, _ = load_target()
        self.assertEqual(len(jobs), 1, 'All ten evaluations must share one queued job.')
        self.assertTrue(jobs[0].result().success)
        self.assertEqual(len(ns['y']), 10)
        np.testing.assert_allclose(ns['y'], np.zeros(10), atol=.15)
        np.testing.assert_allclose(ns['z'], np.zeros(10), atol=1e-9)
''')
TESTS['364'] = ("Approximate Hamiltonian evolution closely enough to implement Hadamard.", '''
class Test(unittest.TestCase):
    def test_trotter_accuracy(self):
        import numpy as np
        from qiskit.quantum_info import Operator
        ns, _ = load_target()
        expected = Operator(np.array([[1,1],[1,-1]])/np.sqrt(2))
        self.assertTrue(ns['u_pauli'].equiv(expected, atol=.02))
        self.assertTrue(ns['u_pauli'].equiv(ns['u_hamil'], atol=.02))
''')
TESTS['377'] = ("Return the Bell state's actual amplitudes, rather than shot counts.", '''
class Test(unittest.TestCase):
    def test_amplitudes_returned(self):
        import math
        from qiskit.quantum_info import Statevector
        ns, _ = load_target()
        result = ns['result']
        self.assertTrue(result.success)
        state = Statevector(result.get_statevector())
        self.assertTrue(state.equiv(Statevector([1/math.sqrt(2),0,0,1/math.sqrt(2)])))
''')
TESTS['401'] = ("Echo waiting-time phase drift so HH remains identity on every input state.", '''
class Test(unittest.TestCase):
    def test_echo_under_static_phase_drift(self):
        import numpy as np
        from qiskit.quantum_info import Operator
        ns, _ = load_target()
        qc = circuits(ns)[-1]
        # Ideal Aer assigns no phase to Delay. Evaluate the stated physical
        # environment explicitly; every delay accumulates the same static drift.
        for omega in (.003, .013, np.pi/500):
            action = np.eye(2, dtype=complex)
            for item in qc.data:
                operation = item[0]
                if operation.name in ('measure', 'barrier'):
                    continue
                if operation.name == 'delay':
                    phase = omega*float(operation.duration)
                    matrix = np.diag([np.exp(-.5j*phase), np.exp(.5j*phase)])
                else:
                    matrix = Operator(operation).data
                action = matrix @ action
            self.assertTrue(Operator(action).equiv(Operator(np.eye(2))),
                            'The waiting-time drift must cancel, up to global phase.')
''')
TESTS['406'] = ("Recover the absolute mean amplitude from the uniform-state projector.", '''
class Test(unittest.TestCase):
    def test_mean_amplitude_observable(self):
        import math
        import numpy as np
        ns, _ = load_target()
        self.assertAlmostEqual(float(ns['absolute_average']), 1/(2*math.sqrt(2)), places=12)
''')

if __name__ == '__main__':
    for number, (intent, body) in TESTS.items():
        path = ROOT / ('issue_' + number) / 'test.py'
        kind = 'STRUCTURAL' if number in ('139','151','162','221','347') else 'WRONG_OUTPUT'
        source = '# intent: ' + intent + '\n# bug_type: ' + kind + '\n' + HEADER + textwrap.dedent(body).lstrip() + FOOTER
        compile(source, str(path), 'exec')
        path.write_text(source, encoding='utf-8')
    print('Created', len(TESTS), 'standalone tests.')
