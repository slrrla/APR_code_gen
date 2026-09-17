"""Scalar composition must retain an operator, with the correct matrix."""
import contextlib
import functools
import io
import os
from pathlib import Path
import runpy
import unittest

MUT = os.environ.get("MUT", str(Path(__file__).with_name("fixed.py")))

@functools.lru_cache(maxsize=1)
def load_target():
    with contextlib.redirect_stdout(io.StringIO()):
        return runpy.run_path(MUT)


import numpy as np
class TestIntent(unittest.TestCase):
    def test_operator_type_and_matrix(self):
        from qiskit.opflow import OperatorBase
        ns = load_target()
        op = ns["my_op"]
        self.assertIsInstance(op, OperatorBase)
        x = 3.5 * np.sqrt(1.5)
        expected = np.diag([4*x, 0]).astype(complex)
        np.testing.assert_allclose(op.to_matrix(), expected, atol=1e-10, rtol=1e-10)
        self.assertEqual(op.num_qubits, 1)

if __name__ == "__main__":
    unittest.main()

