"""Accept the answer's no-go example and exact phase-preserving Qiskit fixes.

Pure Rx/Ry/Rz products have determinant one. Qiskit can also retain the missing
scalar in circuit.global_phase, without adding gates outside that basis.
The reference demonstrates the first case; the question requests the second.
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

    def test_pure_rotation_example_or_exact_phase_preservation(self):
        from qiskit.quantum_info import Operator
        m=target()
        expected=np.diag([1,np.exp(.5j)])
        actual = Operator(m["transpiled"]).data
        np.testing.assert_allclose(np.linalg.det(expected), np.exp(.5j), atol=1e-12)
        self.assertGreater(abs(np.linalg.det(expected) - 1), 0.1)
        if np.allclose(actual, expected, rtol=0, atol=1e-12):
            # An explicit global phase is metadata, not an extra basis gate.
            return
        # Retain the original answer's mathematically valid no-go example.
        # A different SU(2) decomposition may differ from Rz by a minus sign.
        np.testing.assert_allclose(np.linalg.det(actual), 1, rtol=0, atol=1e-12,
            err_msg="Use a pure-rotation no-go example or preserve U1's phase exactly")

if __name__ == "__main__":
    unittest.main()
