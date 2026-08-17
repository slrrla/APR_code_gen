# intent: transpile a 3-qubit GHZ circuit for FakeVigo with optimization_level=3 using a VALID layout_method (e.g. 'noise_adaptive'); 'csp_layout' is not a valid layout method and raises TranspilerError
# bug_type: CRASH
import os, runpy, unittest
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

CASE_DIR = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("MUT", os.path.join(CASE_DIR, "fixed.py"))


def _namespace(path):
    # buggy version raises TranspilerError('Invalid layout method csp_layout') here
    return runpy.run_path(path)


class Test(unittest.TestCase):
    def test_intent(self):
        ns = _namespace(MUT)
        circuits = [v for v in ns.values() if isinstance(v, QuantumCircuit)]
        self.assertTrue(circuits, "no QuantumCircuit produced by the script")

        transpiled = ns.get("transpiled")
        self.assertIsInstance(transpiled, QuantumCircuit,
                              "script must bind a transpiled QuantumCircuit")

        # INTENT: transpilation targets FakeVigo (5 qubits) and keeps the 3 measurements
        self.assertEqual(transpiled.num_qubits, 5)
        self.assertEqual(transpiled.num_clbits, 3)
        self.assertEqual(transpiled.count_ops().get("measure", 0), 3)

        # INTENT: only basis gates of FakeVigo are used after transpilation
        allowed = {"id", "rz", "sx", "x", "cx", "measure", "barrier", "reset", "delay"}
        self.assertTrue(set(transpiled.count_ops()).issubset(allowed),
                        f"unexpected ops: {set(transpiled.count_ops()) - allowed}")

        # INTENT: the logical circuit is a 3-qubit GHZ state -> only '000' and '111', each 0.5
        source = ns.get("qc")
        self.assertIsInstance(source, QuantumCircuit)
        sv = Statevector.from_instruction(source.remove_final_measurements(inplace=False))
        probs = sv.probabilities_dict()
        self.assertEqual(set(probs), {"000", "111"})
        for k in ("000", "111"):
            self.assertAlmostEqual(probs[k], 0.5, places=9)


if __name__ == '__main__':
    unittest.main(argv=[''])
