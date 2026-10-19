"""Retrieve and check every matrix element from the original Aer execution."""
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
    def test_saved_unitary_from_aer(self):
        ns = load_target()
        self.assertTrue(ns["result"].success)
        expected = np.array([[1,1,0,0],[0,0,1,-1],[0,0,1,1],[1,-1,0,0]])/np.sqrt(2)
        actual = np.asarray(ns["unitary"])
        np.testing.assert_allclose(actual, expected, atol=1e-10, rtol=1e-10)
        np.testing.assert_allclose(actual.conj().T @ actual, np.eye(4), atol=1e-10)
        np.testing.assert_allclose(np.asarray(ns["result"].get_unitary(ns["circ"])), expected, atol=1e-10)

if __name__ == "__main__":
    unittest.main()

