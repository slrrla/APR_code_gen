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
    def test_projector_and_solver_conversion(self):
        m = target()
        expected = np.full((2,2), .5)
        np.testing.assert_allclose(m["proj"].data, expected, atol=1e-12)
        np.testing.assert_allclose(m["op"].to_matrix(), expected, atol=1e-12)
        np.testing.assert_allclose(m["spectrum"].eigenvalues, [0], atol=1e-10)
        full = m["NumPyEigensolver"](k=2).compute_eigenvalues(m["op"])
        np.testing.assert_allclose(np.sort(full.eigenvalues), [0,1], atol=1e-10)

if __name__ == "__main__":
    unittest.main()

