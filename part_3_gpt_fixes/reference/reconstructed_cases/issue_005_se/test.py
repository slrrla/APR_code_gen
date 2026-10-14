# intent: migrate Qiskit v0.x QuantumInstance/qiskit.providers.aer execution to Qiskit 1.x (qiskit_aer + backend.run); the program must build H|0> + measure_all and sample counts over {'0','1'} ~50/50
# bug_type: CRASH
import os, runpy, unittest
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

CASE_DIR = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("MUT", os.path.join(CASE_DIR, "fixed.py"))  # code under test


def _run(path):
    # buggy version raises ImportError/ModuleNotFoundError here -> test fails (bug found)
    return runpy.run_path(path)


def _last_circuit(ns):
    cs = [v for v in ns.values() if isinstance(v, QuantumCircuit)]
    assert cs, "no QuantumCircuit produced by the script"
    return cs[-1]


class Test(unittest.TestCase):
    def test_runs_and_produces_counts(self):
        ns = _run(MUT)

        # the migrated script must actually obtain a result object with counts
        result = ns.get("result", None)
        self.assertIsNotNone(result, "script produced no 'result' object")
        counts = result.get_counts()
        self.assertEqual(set(counts), {'0', '1'})
        total = sum(counts.values())
        self.assertEqual(total, 1024)
        # ideal H|0> distribution: 0.5 / 0.5 (loose tolerance for sampling)
        self.assertAlmostEqual(counts['0'] / total, 0.5, delta=0.15)
        self.assertAlmostEqual(counts['1'] / total, 0.5, delta=0.15)

    def test_circuit_intent(self):
        ns = _run(MUT)
        qc = _last_circuit(ns)
        self.assertEqual(qc.num_qubits, 1)

        plain = qc.remove_final_measurements(inplace=False)
        probs = Statevector.from_instruction(plain).probabilities_dict()
        # INTENT: single qubit in equal superposition
        self.assertEqual(set(probs), {'0', '1'})
        for k in ('0', '1'):
            self.assertAlmostEqual(probs[k], 0.5, places=9)


if __name__ == '__main__':
    unittest.main(argv=[''])
