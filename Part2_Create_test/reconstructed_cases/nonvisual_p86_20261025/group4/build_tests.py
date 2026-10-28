"""Materialize reviewed standalone oracles; never edit buggy.py or fixed.py."""
from pathlib import Path
import textwrap

ROOT = Path(__file__).resolve().parents[2]
HEADER = '''# intent: {intent}
# bug_type: {kind}
import contextlib
import io
import os
import runpy
import unittest
from unittest.mock import patch

CASE_DIR = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("MUT", os.path.join(CASE_DIR, "fixed.py"))


def load_target():
    """Observe actual printed objects and text without changing the program."""
    objects = []
    stream = io.StringIO()
    original_print = print

    def observe(*args, **kwargs):
        objects.extend(args)
        return original_print(*args, **kwargs)

    with contextlib.redirect_stdout(stream), patch("builtins.print", observe):
        namespace = runpy.run_path(MUT)
    return namespace, objects, stream.getvalue()


class Test(unittest.TestCase):
'''
END = '\n\nif __name__ == "__main__":\n    unittest.main(argv=[""])\n'


def write(case, intent, body, kind='WRONG_OUTPUT'):
    target = ROOT / case / 'test.py'
    assert not target.exists(), 'Preserve existing test: ' + str(target)
    source = HEADER.format(intent=intent, kind=kind) + textwrap.indent(textwrap.dedent(body).strip(), '    ') + END
    compile(source, str(target), 'exec')
    target.write_text(source, encoding='utf-8')


write('issue_736', 'Calling measurement must return an outcome and the matching collapsed state.', '''
def test_measurement_is_performed(self):
    import numpy as np
    from qiskit.quantum_info import Statevector
    observed = []
    original = Statevector.measure

    def measure(state, *args, **kwargs):
        state.seed(7)
        result = original(state, *args, **kwargs)
        observed.append((state.copy(), result))
        return result

    with patch.object(Statevector, 'measure', measure):
        load_target()
    self.assertEqual(len(observed), 1, 'A method reference does not perform measurement.')
    before, (outcome, collapsed) = observed[0]
    np.testing.assert_allclose(before.probabilities(), [5/9, 4/9], atol=1e-12)
    self.assertIn(outcome, ('0', '1'))
    self.assertTrue(collapsed.equiv(Statevector.from_label(outcome)))
''', 'STRUCTURAL')

write('issue_752', 'The two-qubit feature phase must depend on parity, not only on qubit 1.', '''
def test_complete_feature_map_operator(self):
    import numpy as np
    from qiskit import QuantumCircuit
    from qiskit.quantum_info import Operator
    ns, _, _ = load_target()
    circuits = [v for v in ns.values() if isinstance(v, QuantumCircuit)]
    self.assertTrue(circuits, 'Expose the constructed feature circuit.')
    phi = (np.pi - 0.5) * (np.pi - 0.8)
    # Basis order 00,01,10,11; odd parity receives the ZZ phase.
    phases = np.exp(1j * np.array([0, 1 + 2*phi, 1.6 + 2*phi, 2.6]))
    h2 = np.array([[1,1,1,1], [1,-1,1,-1], [1,1,-1,-1], [1,-1,-1,1]]) / 2
    expected = Operator(np.diag(phases) @ h2)
    self.assertTrue(Operator(circuits[-1]).equiv(expected))
''')

write('issue_774', 'Explicit |10> initialization must produce a successful simulator result.', '''
def test_backend_completes_with_prepared_state(self):
    from qiskit.quantum_info import Statevector
    ns, _, _ = load_target()
    jobs = [v for v in ns.values() if callable(getattr(v, 'result', None))]
    self.assertTrue(jobs, 'Expose the submitted backend job.')
    result = jobs[-1].result()
    self.assertTrue(result.success, str(result))
    self.assertTrue(all(experiment.success for experiment in result.results))
    self.assertTrue(Statevector(result.get_statevector(0)).equiv(Statevector([0,0,1,0])))
''', 'CRASH')

write('issue_791', 'Iterating the output must expose the six constituent gates, including identities.', '''
def test_printed_gates_are_constituents(self):
    from qiskit.circuit import Instruction
    from qiskit.quantum_info import Operator
    import numpy as np
    _, objects, _ = load_target()
    operations = [v for v in objects if isinstance(v, Instruction)]
    self.assertEqual(len(operations), 6, 'Two opaque subcircuits hide the six constituent operations.')
    matrices = [Operator(op) for op in operations]
    identity = Operator(np.eye(2))
    hadamard = Operator(np.array([[1,1], [1,-1]]) / np.sqrt(2))
    self.assertEqual(sum(op.num_qubits == 1 and matrix.equiv(identity) for op, matrix in zip(operations, matrices)), 2)
    self.assertEqual(sum(op.num_qubits == 1 and matrix.equiv(hadamard) for op, matrix in zip(operations, matrices)), 2)
    self.assertEqual(sum(op.name == 'cx' and op.num_qubits == 2 for op in operations), 2)
''', 'STRUCTURAL')

write('issue_797', 'Print only measured 16-bit strings, without dictionary keys/count punctuation.', '''
def test_output_contains_only_measurement_strings(self):
    import qiskit
    original = qiskit.execute

    def execute(*args, **kwargs):
        kwargs.setdefault('seed_simulator', 17)
        kwargs.setdefault('seed_transpiler', 17)
        return original(*args, **kwargs)

    with patch.object(qiskit, 'execute', execute):
        ns, _, text = load_target()
    lines = text.splitlines()
    self.assertTrue(lines)
    self.assertTrue(all(len(line) == 16 and set(line) <= {'0','1'} for line in lines))
    self.assertEqual(len(lines), len(set(lines)))
    # Compare presentation to the actual backend output, not sampled frequencies.
    self.assertEqual(set(lines), set(ns['result'].get_counts()))
''')

write('issue_814', 'An absent measurement key returns zero; a present key retains its actual count.', '''
def test_missing_and_present_count(self):
    from qiskit.result import Result
    # Deterministic backend-result fixtures exercise missing-key handling directly.
    # Circuit execution is real; only the external count dictionary is supplied.
    for counts, expected in (({'000':41}, 0), ({'000':34,'011':7}, 7)):
        with self.subTest(counts=counts), patch.object(Result, 'get_counts', return_value=counts.copy()):
            _, _, text = load_target()
            self.assertEqual(int(text.strip()), expected)
''')

write('issue_823', 'Bell-state joint correlations are XX=+1 and YY=-1, not products of marginals.', '''
def test_joint_bell_correlations(self):
    import re
    import qiskit
    original = qiskit.execute

    def execute(*args, **kwargs):
        kwargs.setdefault('seed_simulator', 11)
        kwargs.setdefault('seed_transpiler', 11)
        return original(*args, **kwargs)

    with patch.object(qiskit, 'execute', execute):
        _, _, text = load_target()
    for label, expected in (('X0X1', 1), ('Y0Y1', -1)):
        match = re.search(r'<' + label + r'>\s*=\s*([-+0-9.eE]+)', text)
        self.assertIsNotNone(match, 'Report the joint correlation ' + label)
        self.assertAlmostEqual(float(match.group(1)), expected, places=10)
''')

write('issue_859', 'Postselection of qubit 0 onto |0> retains only |00> from the Bell state.', '''
def test_projection_for_reproducible_random_streams(self):
    import numpy as np
    from qiskit.quantum_info import Statevector
    original = np.random.default_rng
    # Seed randomness without replacing reset, projection, or the simulated state.
    for seed in (0, 1, 7):
        def generator(value=None):
            return original(seed if value is None else value)
        with self.subTest(seed=seed), patch.object(np.random, 'default_rng', generator):
            _, objects, _ = load_target()
        states = [v for v in objects if isinstance(v, Statevector)]
        self.assertTrue(states, 'Expose the postselected state.')
        self.assertTrue(states[-1].equiv(Statevector([1,0,0,0])), 'Reset is not postselection.')
''')

write('issue_863', 'The full bridge circuit must act correctly on all eight computational basis states.', '''
def test_complete_bridge_matrix(self):
    import numpy as np
    _, objects, _ = load_target()
    matrices = [v for v in objects if isinstance(v, np.ndarray) and v.shape == (8,8)]
    self.assertTrue(matrices, 'Report the complete three-qubit operator.')
    # CNOT(0,1), CNOT(1,2), then the bridge CNOT(2,0).
    # Columns are input 000..111; entries specify their output basis indices.
    expected = np.eye(8)[:, [0,6,7,1,5,3,2,4]]
    np.testing.assert_allclose(matrices[-1], expected, atol=1e-12)
''')

write('issue_870', 'The pulse simulator must finish the assembled one-qubit experiment successfully.', '''
def test_pulse_job_success_and_counts(self):
    ns, _, _ = load_target()
    jobs = [v for v in ns.values() if callable(getattr(v, 'result', None))]
    self.assertTrue(jobs, 'Expose the pulse simulation job.')
    result = jobs[-1].result()
    self.assertTrue(result.success, str(result))
    self.assertEqual(len(result.results), 1)
    self.assertTrue(result.results[0].success)
    counts = result.get_counts(0)
    self.assertTrue(counts)
    self.assertTrue(set(counts) <= {'0','1'})
    self.assertEqual(sum(counts.values()), 1024)
''', 'CRASH')

write('issue_879', 'The reduced state of qubits 3 and 5 is the maximally mixed two-qubit density matrix.', '''
def test_reduced_density_matrix_and_purity(self):
    import numpy as np
    from qiskit.quantum_info import DensityMatrix
    ns, _, _ = load_target()
    reduced = [v for v in ns.values() if isinstance(v, DensityMatrix) and v.data.shape == (4,4)]
    self.assertTrue(reduced, 'A 12-qubit pure state is not the two-qubit reduced density matrix.')
    np.testing.assert_allclose(reduced[-1].data, np.eye(4)/4, atol=1e-10)
    self.assertAlmostEqual(float(np.real(reduced[-1].purity())), 0.25, places=10)
''')

write('issue_892', 'A ten-shot measurement run returns ten individual collapsed statevectors.', '''
def test_all_per_shot_states_are_returned(self):
    import qiskit
    from qiskit.quantum_info import Statevector
    original = qiskit.execute

    def execute(*args, **kwargs):
        kwargs.setdefault('seed_simulator', 12)
        kwargs.setdefault('seed_transpiler', 12)
        return original(*args, **kwargs)

    with patch.object(qiskit, 'execute', execute):
        ns, _, _ = load_target()
    results = [v for v in ns.values() if callable(getattr(v, 'get_counts', None)) and callable(getattr(v, 'data', None))]
    self.assertTrue(results)
    self.assertTrue(results[-1].success)
    lists = [v for v in results[-1].data(0).values() if isinstance(v, (list,tuple)) and len(v) == 10]
    self.assertTrue(lists, 'A final statevector is not a list of ten per-shot states.')
    for value in lists[-1]:
        state = Statevector(value)
        self.assertTrue(state.equiv(Statevector([1,0,0,0])) or state.equiv(Statevector([0,1,0,0])))
''')

write('issue_902', 'Report sampled classical outcomes after execution, rather than Python branch-construction values.', '''
def test_output_is_a_single_measured_outcome(self):
    _, objects, _ = load_target()
    values = [v for v in objects if isinstance(v, list)]
    self.assertTrue(values)
    self.assertEqual(len(values[-1]), 1, 'Both Python branch bodies execute while constructing a circuit.')
    counts = values[-1][0]
    self.assertIsInstance(counts, dict)
    self.assertEqual(sum(counts.values()), 1)
    self.assertTrue(all(len(key) == 2 and set(key) <= {'0','1'} for key in counts))
''')

write('issue_924', 'The requested squared-operator expectation for the Bell state equals 3.61.', '''
def test_squared_operator_expectation(self):
    import numbers
    _, objects, _ = load_target()
    scalars = [complex(v) for v in objects if isinstance(v, numbers.Number)]
    self.assertTrue(scalars, 'Report the expectation value.')
    self.assertAlmostEqual(scalars[-1].real, 3.61, places=10)
    self.assertAlmostEqual(scalars[-1].imag, 0, places=10)
''')

write('issue_974', 'Expose individual Pauli strings or PauliOp terms, with labels XXI, IYY and ZZX.', '''
def test_individual_terms_are_accessible(self):
    from qiskit.quantum_info import Pauli
    _, objects, _ = load_target()
    self.assertEqual(len(objects), 3)
    labels = []
    for term in objects:
        if isinstance(term, str):
            labels.append(term)
        else:
            primitive = getattr(term, 'primitive', term)
            self.assertIsInstance(primitive, Pauli, 'A one-element PauliSumOp still hides the individual Pauli.')
            self.assertEqual(getattr(term, 'coeff', 1), 1)
            labels.append(primitive.to_label())
    self.assertCountEqual(labels, ['XXI','IYY','ZZX'])
''', 'STRUCTURAL')

write('issue_981', 'The SSH hopping Hamiltonian has intracell coupling 1 and intercell coupling 2.', '''
def test_complete_ssh_hamiltonian(self):
    import numpy as np
    ns, _, _ = load_target()
    matrices = [v for v in ns.values() if isinstance(v, np.ndarray) and v.shape == (20,20)]
    self.assertTrue(matrices)
    # Reversing the unit-cell orientation exchanges the two valid intercell
    # layouts. Both describe the same open SSH chain in different bases.
    valid = []
    for orientation in (0, 1):
        expected = np.zeros((20,20), complex)
        for cell in range(10):
            a, b = 2*cell, 2*cell+1
            expected[a,b] = expected[b,a] = 1
        for cell in range(9):
            a, b = ((2*cell+1, 2*cell+2) if orientation == 0 else (2*cell, 2*cell+3))
            expected[a,b] = expected[b,a] = 2
        valid.append(expected)
    self.assertTrue(any(np.allclose(matrices[-1], expected, atol=1e-12) for expected in valid))
''')

write('issue_992', 'The reported QPE ground energy must agree with the Hamiltonian minimum eigenvalue to phase resolution.', '''
def test_qpe_reports_ground_energy(self):
    import re
    import numpy as np
    import qiskit
    from qiskit.utils import algorithm_globals
    algorithm_globals.random_seed = 19
    original = qiskit.execute

    def execute(*args, **kwargs):
        kwargs.setdefault('seed_simulator', 19)
        kwargs.setdefault('seed_transpiler', 19)
        return original(*args, **kwargs)

    with patch.object(qiskit, 'execute', execute):
        ns, _, text = load_target()
    match = re.search(r'QPE-approximated H-eigenvalue:\s*([-+0-9.eE]+)', text)
    self.assertIsNotNone(match)
    exact = float(np.linalg.eigvalsh(ns['Hmat'])[0])
    self.assertAlmostEqual(exact, -1.60671245, places=7)
    self.assertLessEqual(abs(float(match.group(1)) - exact), 2*np.pi/1024)
    self.assertTrue(ns['job'].result().success)
''')

write('issue_1001', 'Appending a second noise error must be quiet while retaining both composed channels.', '''
def test_noise_composition_without_duplicate_warning(self):
    import logging
    import numpy as np
    from qiskit.quantum_info import SuperOp
    records = []

    class Capture(logging.Handler):
        def emit(self, record):
            records.append(record.getMessage())

    handler = Capture()
    logger = logging.getLogger()
    logger.addHandler(handler)
    try:
        ns, _, _ = load_target()
    finally:
        logger.removeHandler(handler)
    self.assertFalse(any('quantum error already exists' in text.lower() for text in records))
    data = ns['myNoiseModel'].to_dict()
    self.assertEqual(len(data['errors']), 1)
    from qiskit.providers.aer.noise.errors import QuantumError
    error = data['errors'][0]
    if hasattr(QuantumError, 'from_dict'):
        combined = QuantumError.from_dict(error)
    else:
        combined = QuantumError(list(zip(error['instructions'], error['probabilities'])))
    expected = ns['error1'].compose(ns['error2'])
    np.testing.assert_allclose(SuperOp(combined).data, SuperOp(expected).data, atol=1e-10)
''')

write('issue_1009', 'Exact and shot-based estimators both respect the Bell-state deterministic correlations.', '''
def test_valid_bell_expectations(self):
    import numpy as np
    from qiskit.utils import algorithm_globals
    algorithm_globals.random_seed = 5
    ns, _, _ = load_target()
    values = np.asarray(ns['observables_results'], float)
    self.assertEqual(values.shape, (3,))
    self.assertTrue(np.all(np.isfinite(values)))
    np.testing.assert_allclose(values[[0,2]], [1,1], atol=1e-10)
    self.assertGreaterEqual(values[1], -1)
    self.assertLessEqual(values[1], 1)
    # The source asks why exact and sampled expectations differ. Both are valid;
    # forcing different sampled numerical values would manufacture an APR bug.
''')

write('issue_1033', 'Both entanglement constructions prepare the same normalized three-qubit GHZ state.', '''
def test_both_constructions_prepare_ghz(self):
    import numpy as np
    from qiskit import QuantumCircuit
    from qiskit.quantum_info import Statevector
    ns, _, _ = load_target()
    circuits = [v for v in ns.values() if isinstance(v, QuantumCircuit)]
    self.assertEqual(len(circuits), 2)
    expected = Statevector(np.array([1,0,0,0,0,0,0,1]) / np.sqrt(2))
    for circuit in circuits:
        self.assertTrue(Statevector.from_instruction(circuit).equiv(expected))
    # Full operators need not be equal just because their action on |000> is.
    # The reconstructed op2 assignment typo is not a source-grounded GHZ bug.
''')

print('Created 20 standalone tests')
