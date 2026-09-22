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
    def test_requested_rotation_basis_and_equivalence_up_to_phase(self):
        from qiskit.quantum_info import Operator
        m=target()
        self.assertLessEqual(set(m["transpiled"].count_ops()), {"rx","ry","rz"})
        actual=Operator(m["transpiled"]).data
        expected=np.diag([1,np.exp(.5j)])
        self.assertTrue(Operator(actual).equiv(Operator(expected)))

    def test_original_requirement_preserve_u1_phase_exactly(self):
        from qiskit.quantum_info import Operator
        m=target()
        expected=np.diag([1,np.exp(.5j)])
        np.testing.assert_allclose(Operator(m["transpiled"]).data,expected,atol=1e-12,
            err_msg="Original question explicitly requires retaining U1 global phase")

if __name__ == "__main__":
    unittest.main()

