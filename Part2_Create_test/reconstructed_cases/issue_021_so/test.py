# intent: execute the nine-qubit measured circuit successfully using the imported execute function
# bug_type: CRASH
import os
import runpy
import unittest

from qiskit import QuantumCircuit


CASE_DIR = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("MUT", os.path.join(CASE_DIR, "fixed.py"))


def _namespace(path):
    return runpy.run_path(path)


class Test(unittest.TestCase):
    def test_circuit_executes_with_expected_structure(self):
        ns = _namespace(MUT)

        circuit = ns.get("circuit")
        self.assertIsInstance(circuit, QuantumCircuit)
        self.assertEqual(circuit.num_qubits, 9)
        self.assertEqual(circuit.num_clbits, 9)

        operation_names = [instruction[0].name for instruction in circuit.data]
        self.assertEqual(operation_names, ["h"] * 9 + ["measure"] * 9)

        self.assertIn("measure", ns)
        job = ns["measure"]
        result = job.result()
        self.assertTrue(result.success)


if __name__ == "__main__":
    unittest.main(argv=[""])
