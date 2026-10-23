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
    def test_operator_dimension_and_diagonality(self):
        m=target()
        data=m["op"].data
        self.assertEqual(data.shape, (1024,1024))
        np.testing.assert_allclose(data, np.diag(np.diag(data)), atol=1e-12)
        np.testing.assert_allclose(abs(np.diag(data)), np.ones(1024), atol=1e-12)

    def test_z_acts_on_requested_qiskit_qubits_i_plus_one_to_j_minus_one(self):
        m=target()
        diagonal=np.diag(m["op"].data)
        # Qiskit qubit k is binary bit k (least significant bit is qubit zero).
        expected=np.array([(-1)**sum((basis >> q)&1 for q in range(3,8))
                           for basis in range(1024)])
        np.testing.assert_allclose(diagonal, expected, atol=1e-12,
            err_msg="Requested Z on qubits 3..7, not on qubits 2..6")

if __name__ == "__main__":
    unittest.main()

