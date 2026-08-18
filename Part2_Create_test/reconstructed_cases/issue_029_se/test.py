# intent: Apply a two-qubit |++> sub-circuit to qubits 0 and 1 of a four-qubit circuit already in |1111>.
# bug_type: CRASH
import os
import runpy
import unittest

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector


CASE_DIR = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("MUT", os.path.join(CASE_DIR, "fixed.py"))


def _circuit(path):
    namespace = runpy.run_path(path)
    circuits = [
        value for value in namespace.values()
        if isinstance(value, QuantumCircuit)
    ]
    if not circuits:
        raise AssertionError("no QuantumCircuit produced by the script")
    return circuits[-1]


class Test(unittest.TestCase):
    def test_subcircuit_is_applied_to_existing_qubits(self):
        circuit = _circuit(MUT)

        self.assertEqual(circuit.num_qubits, 4)
        self.assertEqual(
            [instruction.operation.name for instruction in circuit.data],
            ["x", "x", "x", "x", "h", "h"],
        )

        probabilities = Statevector.from_instruction(circuit).probabilities_dict()
        expected = {"1100", "1101", "1110", "1111"}

        self.assertEqual(set(probabilities), expected)
        for state in expected:
            self.assertAlmostEqual(probabilities[state], 0.25, places=9)


if __name__ == "__main__":
    unittest.main(argv=[""])
