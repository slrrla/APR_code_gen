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
    def test_actual_qasm_snapshot_contains_bell_state(self):
        m=target()
        self.assertTrue(m["job_result"].success)
        state=np.asarray(m["statevector"],dtype=complex)
        expected=np.array([1,0,0,1])/np.sqrt(2)
        np.testing.assert_allclose(state,expected,atol=1e-10)
        snapshot=m["job_result"].data(m["qc"])["snapshots"]["statevector"]["final"][0]
        np.testing.assert_allclose(snapshot,state,atol=1e-12)

if __name__ == "__main__":
    unittest.main()

