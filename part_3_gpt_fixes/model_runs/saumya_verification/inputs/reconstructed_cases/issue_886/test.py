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
    def test_actual_aer_execution_and_zero_control(self):
        m = target()
        result = m["job"].result()
        self.assertTrue(result.success)
        self.assertEqual(result.get_counts(), {"00":1024})

    def test_transpilation_preserves_full_controlled_rotation(self):
        from qiskit.quantum_info import Operator
        m = target()
        qc = m["transpile_circ"].remove_final_measurements(inplace=False)
        expected = np.eye(4, dtype=complex)
        expected[np.ix_([1,3],[1,3])] = [[2**-.5,-1j*2**-.5],[-1j*2**-.5,2**-.5]]
        np.testing.assert_allclose(Operator(qc).data, expected, atol=1e-10)

if __name__ == "__main__":
    unittest.main()

