"""Intent: import standalone Aer and build a measurable Hadamard circuit."""
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


import numpy as np
from qiskit.quantum_info import Statevector

class TestIntent(unittest.TestCase):
    def test_aer_backend_and_hadamard(self):
        ns = load_target()
        qc = ns["qc"]
        self.assertEqual((qc.num_qubits, qc.num_clbits), (1,1))
        self.assertEqual([op.name for op, _, _ in qc.data], ["h", "measure"])
        self.assertEqual(qc.data[-1][1], [qc.qubits[0]])
        self.assertEqual(qc.data[-1][2], [qc.clbits[0]])
        np.testing.assert_allclose(
            Statevector.from_instruction(qc.remove_final_measurements(inplace=False)).probabilities(),
            [0.5,0.5], atol=1e-12, rtol=0)
        result = ns["backend"].run(qc, shots=2048, seed_simulator=917).result()
        self.assertTrue(result.success)
        counts = result.get_counts()
        self.assertEqual(set(counts), {"0","1"})
        self.assertEqual(sum(counts.values()), 2048)
        self.assertAlmostEqual(counts["0"]/2048, 0.5, delta=0.08)

if __name__ == "__main__":
    unittest.main()

