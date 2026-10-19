"""Intent: use Aer Statevector results as arrays when averaging PQC densities.
The full unmodified 2048-sample entry point is executed with a fixed seed.
Analytic checks allow the source's explicit five-decimal amplitude rounding.
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
from unittest.mock import patch

class TestIntent(unittest.TestCase):
    def test_integral_statevector_conversion(self):
        random_state = np.random.get_state()
        try:
            np.random.seed(917)
            ns = load_target()
            for angle in (0.0, np.pi/2, np.pi):
                with patch.object(np.random, "uniform", return_value=np.array([angle])):
                    rho = ns["pqc_integral"](2, ns["ansatz2"], 1, 2)
                c,s = np.cos(angle/2),np.sin(angle/2)
                state = np.array([c,-1j*s,-1j*s,c])/np.sqrt(2)
                expected = np.outer(state,state.conj())
                np.testing.assert_allclose(rho, expected, atol=3e-5, rtol=0)
                np.testing.assert_allclose(rho,rho.conj().T,atol=1e-12,rtol=0)
                self.assertAlmostEqual(float(np.trace(rho).real),1.0,delta=3e-5)
            with patch.object(np.random,"uniform",side_effect=[np.array([0.0]),np.array([np.pi])]):
                average = ns["pqc_integral"](2,ns["ansatz2"],1,2)
            expected = np.array([[1,0,0,1],[0,1,1,0],[0,1,1,0],[1,0,0,1]])/4
            np.testing.assert_allclose(average,expected,atol=3e-5,rtol=0)
        finally:
            np.random.set_state(random_state)

if __name__ == "__main__":
    unittest.main()

