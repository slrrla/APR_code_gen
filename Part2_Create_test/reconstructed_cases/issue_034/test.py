# intent: Import Aer from qiskit_aer and construct a one-qubit Hadamard-measurement circuit.
# bug_type: CRASH
import os
import runpy
import unittest

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector


CASE_DIR = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("MUT", os.path.join(CASE_DIR, "fixed.py"))


def _load(path):
    return runpy.run_path(path)


def _circuit(path):
    namespace = _load(path)
    circuits = [
        value for value in namespace.values() if isinstance(value, QuantumCircuit)
    ]
    if not circuits:
        raise AssertionError("no QuantumCircuit produced by the script")
    return circuits[-1]


class Test(unittest.TestCase):
    def test_aer_import_and_circuit(self):
        qc = _circuit(MUT)

        self.assertEqual(qc.num_qubits, 1)
        self.assertEqual(qc.num_clbits, 1)
        self.assertEqual(
            [instruction.operation.name for instruction in qc.data],
            ["h", "measure"],
        )

        circuit_without_measurements = qc.remove_final_measurements(inplace=False)
        probabilities = Statevector.from_instruction(
            circuit_without_measurements
        ).probabilities_dict()

        self.assertEqual(set(probabilities), {"0", "1"})
        self.assertAlmostEqual(probabilities["0"], 0.5, places=9)
        self.assertAlmostEqual(probabilities["1"], 0.5, places=9)


if __name__ == "__main__":
    unittest.main(argv=[""])
