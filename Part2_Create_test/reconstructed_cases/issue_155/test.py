"""Intent: trace out all qubits in reg2 and reg4, keeping reg1 and reg3."""
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

class TestIntent(unittest.TestCase):
    def test_reduced_density_matrix(self):
        ns = load_target()
        rho = np.asarray(ns["density_matrix"].data)
        # Remaining order: reg3[1], reg3[0], reg1[1], reg1[0].
        # Each first qubit is maximally mixed; each second qubit is |0>.
        expected = np.zeros((16,16), dtype=complex)
        expected[[0,1,4,5],[0,1,4,5]] = 0.25
        self.assertEqual(rho.shape, (16,16))
        np.testing.assert_allclose(rho, expected, atol=1e-12, rtol=0)
        self.assertAlmostEqual(float(np.trace(rho).real), 1.0, places=12)
        self.assertGreaterEqual(np.linalg.eigvalsh(rho).min(), -1e-12)

if __name__ == "__main__":
    unittest.main()

