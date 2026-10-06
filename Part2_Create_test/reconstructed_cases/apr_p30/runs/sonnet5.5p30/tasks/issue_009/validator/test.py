"""Intent: valid layout selection must compile the GHZ circuit for the backend."""
import contextlib
import io
import os
from pathlib import Path
import runpy
import unittest

CASE_DIR = Path(__file__).resolve().parent
MUT = os.environ.get("MUT", str(CASE_DIR / "fixed.py"))

def load_target():
    with contextlib.redirect_stdout(io.StringIO()):
        return runpy.run_path(MUT)


from qiskit.quantum_info import Statevector

class TestIntent(unittest.TestCase):
    def test_transpiled_ghz_measurement_distribution(self):
        ns = load_target()
        qc = ns["transpiled"]
        self.assertEqual(qc.num_qubits, 5)
        self.assertEqual(qc.num_clbits, 3)
        mapping = [(qc.qubits.index(q[0]), qc.clbits.index(c[0]))
                   for op, q, c in qc.data if op.name == "measure"]
        self.assertEqual(len(mapping), 3)
        self.assertEqual({c for _, c in mapping}, {0, 1, 2})
        allowed = set(ns["backend"].configuration().basis_gates) | {"measure", "barrier"}
        self.assertTrue(set(qc.count_ops()).issubset(allowed))
        state = Statevector.from_instruction(qc.remove_final_measurements(inplace=False))
        measured = {}
        for basis, p in enumerate(state.probabilities()):
            if p < 1e-12:
                continue
            outcome = sum(((basis >> q) & 1) << c for q, c in mapping)
            measured[outcome] = measured.get(outcome, 0.0) + float(p)
        self.assertEqual(set(measured), {0, 7})
        self.assertAlmostEqual(measured[0], 0.5, places=9)
        self.assertAlmostEqual(measured[7], 0.5, places=9)

if __name__ == "__main__":
    unittest.main()

