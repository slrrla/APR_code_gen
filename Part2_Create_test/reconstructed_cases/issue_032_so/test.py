# intent: A Bell-state circuit executed with the QASM simulator must return ten
# measurement-memory entries, each being either 00 or 11.
# bug_type: CRASH
import os
import runpy
import unittest

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector


CASE_DIR = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("MUT", os.path.join(CASE_DIR, "fixed.py"))


def _namespace(path):
    return runpy.run_path(path)


def _circuit(namespace):
    circuits = [
        value for value in namespace.values() if isinstance(value, QuantumCircuit)
    ]
    if not circuits:
        raise AssertionError("no QuantumCircuit produced by the script")
    return circuits[-1]


class Test(unittest.TestCase):
    def test_intended_memory_results(self):
        namespace = _namespace(MUT)

        memory = namespace.get("memory")
        self.assertIsInstance(memory, list)
        self.assertEqual(len(memory), 10)
        self.assertTrue(set(memory).issubset({"00", "11"}))

        qc = _circuit(namespace)
        circuit_without_measurements = qc.remove_final_measurements(inplace=False)
        probabilities = Statevector.from_instruction(
            circuit_without_measurements
        ).probabilities()

        self.assertAlmostEqual(probabilities[0], 0.5, places=9)
        self.assertAlmostEqual(probabilities[1], 0.0, places=9)
        self.assertAlmostEqual(probabilities[2], 0.0, places=9)
        self.assertAlmostEqual(probabilities[3], 0.5, places=9)


if __name__ == "__main__":
    unittest.main(argv=[""])
