"""Verify X tensor I tensor Z without assuming that composition itself is buggy."""
import contextlib
import functools
import io
import os
from pathlib import Path
import runpy
import unittest
import numpy as np

MUT = os.environ.get("MUT", str(Path(__file__).with_name("fixed.py")))

@functools.lru_cache(maxsize=1)
def load_target():
    with contextlib.redirect_stdout(io.StringIO()):
        return runpy.run_path(MUT)


class TestIntent(unittest.TestCase):
    def test_all_supplied_operator_constructions(self):
        ns = load_target()
        expected = np.zeros((8,8),complex)
        for basis in range(8):
            expected[basis^4,basis] = (-1)**(basis&1)
        outputs = [ns["result"]] if "result" in ns else [ns[key] for key in ("op","result_a","result_b","result_c")]
        for index, op in enumerate(outputs):
            with self.subTest(construction=index):
                np.testing.assert_allclose(op.data,expected,atol=1e-10)
                np.testing.assert_allclose(op.data.conj().T@op.data,np.eye(8),atol=1e-10)

if __name__ == "__main__":
    unittest.main()

