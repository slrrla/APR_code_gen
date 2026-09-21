"""Conceptual example, NOT an exact-phase U1 repair or standard APR sample.

The original answer proves a no-go result for pure rotation products.
Verify its Rz example and explicitly retain the exact-phase limitation.
"""
import contextlib
import functools
import io
import os
from pathlib import Path
import runpy
import unittest
import numpy as np

@functools.lru_cache(None)
def target():
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        namespace = runpy.run_path(os.environ.get("MUT", str(Path(__file__).with_name("fixed.py"))))
    namespace["_stdout"] = output.getvalue()
    return namespace

class Regression(unittest.TestCase):
    def test_requested_rotation_basis_and_equivalence_up_to_phase(self):
        from qiskit.quantum_info import Operator
        m=target()
        self.assertLessEqual(set(m["transpiled"].count_ops()), {"rx","ry","rz"})
        actual=Operator(m["transpiled"]).data
        expected=np.diag([1,np.exp(.5j)])
        self.assertTrue(Operator(actual).equiv(Operator(expected)))

    def test_no_go_determinant_and_explicit_missing_phase(self):
        from qiskit.quantum_info import Operator
        m=target()
        expected=np.diag([1,np.exp(.5j)])
        actual = Operator(m["transpiled"]).data
        np.testing.assert_allclose(np.linalg.det(actual), 1, atol=1e-12)
        np.testing.assert_allclose(np.linalg.det(expected), np.exp(.5j), atol=1e-12)
        self.assertGreater(abs(np.linalg.det(expected) - 1), 0.1)
        self.assertFalse(np.allclose(actual, expected, atol=1e-12))
        np.testing.assert_allclose(np.exp(.25j) * actual, expected, atol=1e-12)

if __name__ == "__main__":
    unittest.main()
