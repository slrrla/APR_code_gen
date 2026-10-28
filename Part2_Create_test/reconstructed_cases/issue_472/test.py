# intent: Return a Hermitian generator H satisfying U=exp(iH) for four-qubit QFT.
# bug_type: WRONG_OUTPUT
import contextlib
import io
import os
import runpy
import unittest

CASE_DIR = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("MUT", os.path.join(CASE_DIR, "fixed.py"))

import numpy as np
from scipy.linalg import expm

class Test(unittest.TestCase):
    def test_hermitian_generator_and_evolution(self):
        with contextlib.redirect_stdout(io.StringIO()):
            ns = runpy.run_path(MUT)
        h, unitary = np.asarray(ns['H']), np.asarray(ns['U'])
        self.assertEqual(h.shape, (16,16))
        np.testing.assert_allclose(h, h.conj().T, atol=1e-8, rtol=0)
        # The answer explicitly defines the convention U = exp(+i H).
        np.testing.assert_allclose(expm(1j * h), unitary, atol=1e-8, rtol=0)

if __name__ == "__main__":
    unittest.main(argv=[""])
