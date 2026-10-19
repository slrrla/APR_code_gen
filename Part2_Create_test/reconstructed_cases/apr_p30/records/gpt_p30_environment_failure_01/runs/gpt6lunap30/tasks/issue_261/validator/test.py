"""Intent: construct the Hamiltonian XXX - 2 XZX + 3 XIX from its fixed string.
Only the reviewed, hardcoded expression in the source is evaluated.
"""
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
    def test_hamiltonian_coefficients_and_matrix(self):
        ns = load_target()
        x = np.array([[0,1],[1,0]],dtype=complex)
        z = np.diag([1,-1])
        identity = np.eye(2)
        expected = np.kron(np.kron(x,x),x)-2*np.kron(np.kron(x,z),x)+3*np.kron(np.kron(x,identity),x)
        actual = np.asarray(ns["hamiltonian"].to_matrix())
        self.assertEqual(actual.shape,(8,8))
        np.testing.assert_allclose(actual,expected,atol=1e-12,rtol=0)
        np.testing.assert_allclose(actual,actual.conj().T,atol=1e-12,rtol=0)

if __name__ == "__main__":
    unittest.main()

