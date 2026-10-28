"""Build reviewed intent-based regression tests for the first selected group."""
from pathlib import Path
import hashlib
import json

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
HEADER = '''"""Intent-based regression against unmodified MUT; defaults to sibling fixed.py."""
import contextlib
import io
import os
from pathlib import Path
import runpy
import unittest
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator, Statevector

MUT = os.environ.get("MUT", str(Path(__file__).with_name("fixed.py")))

def load_target():
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        namespace = runpy.run_path(MUT)
    namespace["_stdout"] = output.getvalue()
    return namespace

'''
FOOTER = '''
if __name__ == "__main__":
    unittest.main()
'''

TESTS = {
'issue_002': '''class Regression(unittest.TestCase):
    def test_count_only_quantum_register_bits(self):
        m = load_target()
        self.assertEqual(m["qc"].num_qubits, 12)
        self.assertEqual(m["qc"].num_clbits, 2)
        self.assertEqual(m["num_qubits"], 12)
        self.assertEqual(m["_stdout"].strip(), "12")
''',
'issue_010_se': '''from unittest.mock import patch

class Regression(unittest.TestCase):
    def test_results_retain_submission_order_under_reverse_completion(self):
        # Control only the scheduler's legal completion order; every worker runs.
        def reverse_completion(futures):
            return iter(sorted(list(futures), key=lambda f: f.result()["name"], reverse=True))
        with patch("concurrent.futures.as_completed", reverse_completion):
            m = load_target()
        self.assertEqual([r["name"] for r in m["results"]],
                         ["circuit_0", "circuit_1", "circuit_2", "circuit_3"])
        self.assertEqual(m["_stdout"].strip().splitlines(),
                         ["circuit_0 circuit_0", "circuit_1 circuit_1",
                          "circuit_2 circuit_2", "circuit_3 circuit_3"])
''',
'issue_011': '''class Regression(unittest.TestCase):
    def test_shor_21_resources_and_controlled_modular_exponentiation(self):
        m = load_target()
        qc = m["qc"]
        self.assertEqual((qc.num_qubits, qc.num_clbits), (15, 10))
        # Five work qubits encode 0..20; ten controls resolve the period.
        stages = []
        for item in qc.data:
            op, qargs = item[0], item[1]
            positions = [qc.qubits.index(q) for q in qargs]
            if any(q >= 10 for q in positions) and len(positions) > 1:
                stages.append((op, positions))
        self.assertEqual(len(stages), 10)
        for k, (op, positions) in enumerate(stages):
            self.assertEqual(set(positions), set(range(10, 15)) | {k})
            actual = Operator(op).data
            expected = np.zeros((64, 64), complex)
            multiplier = pow(4, 2 ** k, 21)
            for control in (0, 1):
                for x in range(32):
                    y = multiplier * x % 21 if control and x < 21 else x
                    before = sum(((x >> j) & 1) << positions.index(10+j) for j in range(5))
                    before |= control << positions.index(k)
                    after = sum(((y >> j) & 1) << positions.index(10+j) for j in range(5))
                    after |= control << positions.index(k)
                    expected[after, before] = 1
            np.testing.assert_allclose(actual, expected, atol=1e-12)
        measurements = [(qc.qubits.index(item[1][0]), qc.clbits.index(item[2][0]))
                        for item in qc.data if item[0].name == "measure"]
        self.assertEqual(measurements, [(i, i) for i in range(10)])
''',
'issue_015': '''from unittest.mock import patch
from qiskit.result import Result
import qiskit

class Regression(unittest.TestCase):
    def test_inverse_shadow_map_matches_every_actual_local_measurement(self):
        draws, outcomes, circuits = [], [], []
        randint = np.random.randint
        get_counts = Result.get_counts
        assemble = qiskit.assemble
        def record_draw(*args, **kwargs):
            value = randint(*args, **kwargs)
            if np.asarray(value).shape == (2,):
                draws.append(np.asarray(value).copy())
            return value
        def record_counts(result, *args, **kwargs):
            value = get_counts(result, *args, **kwargs)
            outcomes.append(dict(value))
            return value
        def seeded_assemble(circuit, *args, **kwargs):
            circuits.append(circuit.copy())
            kwargs.setdefault("seed_simulator", 15)
            return assemble(circuit, *args, **kwargs)
        # Observation-only wrappers: all 300 quantum simulations execute normally.
        with patch.object(np.random, "randint", record_draw), patch.object(Result, "get_counts", record_counts), patch.object(qiskit, "assemble", seeded_assemble):
            m = load_target()
        self.assertEqual(len(draws), 300)
        self.assertEqual(len(outcomes), 300)
        self.assertEqual(len(circuits), 300)
        h = np.array([[1, 1], [1, -1]], complex) / np.sqrt(2)
        rotations = [h, h @ np.diag([1, -1j]), np.eye(2)]
        bell_preparation = np.array([[1,1,0,0], [0,0,1,-1], [0,0,1,1], [1,-1,0,0]], complex) / np.sqrt(2)
        expected = np.zeros((4, 4), complex)
        for bases, counts, circuit in zip(draws, outcomes, circuits):
            np.testing.assert_allclose(Operator(circuit.remove_final_measurements(inplace=False)).data,
                np.kron(rotations[int(bases[1])], rotations[int(bases[0])]) @ bell_preparation,
                atol=1e-12, err_msg="The Y measurement must apply S-dagger followed by H")
            self.assertEqual(sum(counts.values()), 1)
            bits = next(iter(counts)).replace(" ", "")
            self.assertEqual(len(bits), 2)
            factors = []
            for q in (0, 1):
                b = int(bits[-1-q])
                projector = np.diag([1-b, b])
                u = rotations[int(bases[q])]
                factors.append(3 * u.conj().T @ projector @ u - np.eye(2))
            expected += np.kron(factors[1], factors[0])
        expected /= 300
        np.testing.assert_allclose(m["record_rho"], expected, atol=1e-12,
            err_msg="Each inverse-map factor must use its own qubit outcome in Qiskit little-endian order")
        self.assertAlmostEqual(np.trace(m["record_rho"]).real, 1.0, places=10)
''',
'issue_019_so': '''class Regression(unittest.TestCase):
    def test_actual_executed_memory_contains_teleported_one(self):
        m = load_target()
        memory = m["job"].get_memory()
        self.assertEqual(len(memory), 1)
        self.assertEqual(len(memory[0]), 3)
        self.assertEqual(memory[0][0], "1", "c2 must record the teleported |1> state")
        self.assertEqual(m["result"], memory[0])
''',
'issue_023': '''class Regression(unittest.TestCase):
    def test_zero_angle_ansatz_is_identity_on_every_input(self):
        m = load_target()
        np.testing.assert_allclose(Operator(m["gateEvolver"]).data, np.eye(8), atol=1e-12)
        np.testing.assert_allclose(m["psiTest0"].data, [0,0,1,0,0,0,0,0], atol=1e-12)
''',
'issue_024_se': '''class Regression(unittest.TestCase):
    def test_export_ungroups_custom_gate_and_preserves_full_operator(self):
        m = load_target()
        qc = QuantumCircuit.from_qasm_str(m["qasm_str"])
        self.assertEqual([item[0].name for item in qc.data], ["h", "cx"])
        expected = np.array([[1,1,0,0], [0,0,1,-1], [0,0,1,1], [1,-1,0,0]], complex) / np.sqrt(2)
        np.testing.assert_allclose(Operator(qc).data, expected, atol=1e-12)
''',
'issue_029_so': '''import sys
from unittest.mock import patch

class Regression(unittest.TestCase):
    def test_install_command_targets_current_notebook_interpreter(self):
        # Offline command-construction test. Installation itself is never executed.
        with patch("subprocess.call", return_value=0) as invoked:
            load_target()
        commands = [call.args[0] for call in invoked.call_args_list]
        self.assertTrue(any(isinstance(c, (tuple, list)) and list(c[:4]) ==
                            [sys.executable, "-m", "pip", "install"] and "qiskit" in c[4:]
                            for c in commands), "Install into the running notebook kernel's interpreter")
''',
'issue_030_se': '''class Regression(unittest.TestCase):
    def test_all_ten_compositions_accumulate_on_qubits_two_and_three(self):
        m = load_target()
        qc = m["qcom"]
        self.assertEqual((qc.num_qubits, qc.num_clbits), (8, 8))
        h = np.array([[1,1],[1,-1]], complex) / np.sqrt(2)
        crz = np.diag([1, np.exp(-1j*np.pi/4), 1, np.exp(1j*np.pi/4)])
        block = crz @ np.kron(np.eye(2), h)
        expected = np.kron(np.eye(16), np.kron(np.linalg.matrix_power(block, 10), np.eye(4)))
        np.testing.assert_allclose(Operator(qc).data, expected, atol=1e-11)
''',
'issue_048': '''class Regression(unittest.TestCase):
    def test_controlled_s_and_t_have_exact_relative_phases(self):
        m = load_target()
        expected = np.diag([1, 1, 1, np.exp(3j*np.pi/4)])
        np.testing.assert_allclose(Operator(m["circuit"]).data, expected, atol=1e-12)
''',
'issue_050': '''class Regression(unittest.TestCase):
    def test_reports_actual_resolved_simulation_method(self):
        m = load_target()
        result = m["simulation_run"].result()
        self.assertTrue(result.success)
        method = result.results[0].metadata["method"]
        self.assertIn(method, {"statevector", "density_matrix", "stabilizer", "extended_stabilizer",
                               "matrix_product_state", "unitary", "superop", "tensor_network"})
        self.assertEqual(m["_stdout"].strip(), method)
''',
'issue_051_se': '''class Regression(unittest.TestCase):
    def test_oracle_marks_only_eleven_and_grover_finds_it(self):
        m = load_target()
        np.testing.assert_allclose(Operator(m["oracle"]()).data, np.diag([1,1,1,-1]), atol=1e-12)
        state = Statevector.from_instruction(m["qc"].remove_final_measurements(inplace=False))
        np.testing.assert_allclose(state.probabilities(), [0,0,0,1], atol=1e-12)
        counts = m["result"].get_counts()
        self.assertEqual(counts, {"11": 1024})
''',
'issue_058_so': '''class Regression(unittest.TestCase):
    def test_one_local_job_contains_three_successful_circuit_results(self):
        m = load_target()
        result = m["job"].result()
        self.assertTrue(result.success)
        self.assertEqual(len(result.results), 3)
        for i, experiment in enumerate(result.results):
            self.assertTrue(experiment.success)
            counts = result.get_counts(i)
            self.assertEqual(set(counts), {"11"})
            self.assertEqual(sum(counts.values()), experiment.shots)
            self.assertGreater(experiment.shots, 0)
''',
'issue_059_se': '''from collections import Counter
from unittest.mock import patch
from qiskit_aer import AerSimulator

class Regression(unittest.TestCase):
    def test_marginal_counts_sum_actual_qubits_zero_and_one(self):
        run = AerSimulator.run
        def seeded(backend, *args, **kwargs):
            kwargs.setdefault("seed_simulator", 59)
            return run(backend, *args, **kwargs)
        with patch.object(AerSimulator, "run", seeded):
            m = load_target()
        expected = Counter()
        for bitstring, count in m["res"].items():
            self.assertEqual(len(bitstring), 4)
            expected[bitstring[-2:]] += count
        self.assertEqual(m["new_counts"], dict(expected))
        self.assertEqual(sum(m["new_counts"].values()), 1024)
''',
'issue_075': '''class Regression(unittest.TestCase):
    def test_full_register_barrier_separates_the_two_gate_layers(self):
        qc = load_target()["qp"]
        before, after, seen = [], [], False
        for item in qc.data:
            op, qargs = item[0], item[1]
            positions = tuple(qc.qubits.index(q) for q in qargs)
            if op.name == "barrier":
                self.assertEqual(set(positions), set(range(8)))
                seen = True
            elif op.name == "cx":
                (after if seen else before).append(positions)
            else:
                self.fail("Unexpected operation in the specified CNOT layers: " + op.name)
        self.assertTrue(seen, "A barrier must prevent scheduling across the two requested steps")
        self.assertEqual(before, [(0,1), (2,3), (4,5), (6,7)])
        self.assertEqual(after, [(1,2), (3,4), (5,6)])
''',
'issue_077_so': '''class Regression(unittest.TestCase):
    def test_half_adder_records_sum_zero_and_carry_one_for_one_plus_one(self):
        qc = load_target()["circuit"]
        self.assertEqual((qc.num_qubits, qc.num_clbits), (3, 2))
        state = Statevector.from_instruction(qc.remove_final_measurements(inplace=False))
        expected = np.zeros(8)
        expected[5] = 1  # q2=carry=1, q1=sum=0, preserved q0=1.
        np.testing.assert_allclose(state.data, expected, atol=1e-12)
        measurements = [(qc.qubits.index(item[1][0]), qc.clbits.index(item[2][0]))
                        for item in qc.data if item[0].name == "measure"]
        self.assertEqual(measurements, [(1,0), (2,1)])
''',
'issue_093': '''from unittest.mock import patch
import shlex

class Regression(unittest.TestCase):
    def test_notebook_repository_is_fetched_before_local_package_install(self):
        # Offline workflow inspection only: never run pip, git, shell or network.
        with patch("subprocess.run") as invoked:
            load_target()
        commands = [call.args[0] for call in invoked.call_args_list]
        texts = [" ".join(c) if isinstance(c, (list, tuple)) else c for c in commands]
        clones = [i for i, c in enumerate(texts) if "git clone" in c and
                  "github.com/qiskit-community/qiskit-textbook" in c]
        installs = [i for i, c in enumerate(texts) if "pip install" in c and
                    "./qiskit-textbook-src" in c and "git+" not in c]
        self.assertTrue(clones, "Fetch the repository containing the actual notebooks")
        self.assertTrue(installs, "Install the package from the cloned local source")
        self.assertLess(clones[0], installs[0])
''',
'issue_095': '''from unittest.mock import patch

class Regression(unittest.TestCase):
    def test_observation_samples_both_branches_without_measuring_state(self):
        for random_value, expected_bit in ((0.25, 0), (0.75, 1)):
            with self.subTest(random_value=random_value), patch("random.random", return_value=random_value):
                m = load_target()
                self.assertNotIn("measure", m["qc"].count_ops())
                np.testing.assert_allclose(np.asarray(m["statevector"]),
                                           np.array([1,1])/np.sqrt(2), atol=1e-12)
                self.assertAlmostEqual(m["prob0"], 0.5, places=12)
                self.assertEqual(m["x"], expected_bit)
''',
'issue_117': '''class Regression(unittest.TestCase):
    def test_actual_aer_result_exposes_saved_bell_statevector(self):
        m = load_target()
        result = m["psi_out_complex"]
        self.assertTrue(result.success)
        state = np.asarray(result.get_statevector(), complex)
        np.testing.assert_allclose(state, np.array([1,0,0,1])/np.sqrt(2), atol=1e-12)
''',
'issue_125': '''class Regression(unittest.TestCase):
    def test_more_than_one_million_shots_are_actually_returned(self):
        m = load_target()
        result = m["result"]
        self.assertTrue(result.success)
        counts = result.get_counts()
        self.assertEqual(sum(counts.values()), 1000001)
        self.assertEqual(set(counts), {"0", "1"})
        # Broad physical sanity bound, never a golden random count.
        self.assertLess(abs(counts["0"] / 1000001 - 0.5), 0.02)
''',
'issue_133': '''class Regression(unittest.TestCase):
    def test_modern_imports_and_real_bell_simulation(self):
        m = load_target()
        self.assertTrue(m["result"].success)
        counts = m["result"].get_counts()
        self.assertEqual(set(counts), {"00", "11"})
        self.assertEqual(sum(counts.values()), 1024)
        state = Statevector.from_instruction(m["qc"].remove_final_measurements(inplace=False))
        np.testing.assert_allclose(state.data, np.array([1,0,0,1])/np.sqrt(2), atol=1e-12)
''',
}

def main():
    records = []
    for case, body in TESTS.items():
        target = ROOT / case / 'test.py'
        if target.exists():
            backup = OUT / 'previous_tests' / case / 'test.py'
            backup.parent.mkdir(parents=True, exist_ok=True)
            if not backup.exists():
                backup.write_bytes(target.read_bytes())
        text = HEADER + body + FOOTER
        compile(text, str(target), 'exec')
        target.write_text(text, encoding='utf-8')
        records.append({'case': case, 'test': str(target), 'sha256': hashlib.sha256(target.read_bytes()).hexdigest()})
    case = 'issue_018_so'
    target = ROOT / case / 'test.py'
    records.append({'case': case, 'test': str(target), 'sha256': hashlib.sha256(target.read_bytes()).hexdigest(), 'preserved': True})
    (OUT / 'tests_manifest.json').write_text(json.dumps(records, indent=2), encoding='utf-8')
    print('Created', len(TESTS), 'tests; preserved issue_018_so')

if __name__ == '__main__':
    main()
