"""Regression tests against the unmodified MUT (default: sibling fixed.py)."""
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
    def test_exact_negative_h_tensor_h_not_just_global_equivalence(self):
        from qiskit.quantum_info import Operator, Statevector
        m=target()
        H=np.array([[1,1],[1,-1]])/np.sqrt(2)
        expected=-np.kron(H,H)
        for name in ("qc","qc2"):
            with self.subTest(circuit=name):
                np.testing.assert_allclose(Operator(m[name]).data, expected, atol=1e-12)
                np.testing.assert_allclose(Statevector(m[name]).data, np.full(4,-.5), atol=1e-12)

if __name__ == "__main__":
    unittest.main()

