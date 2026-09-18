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
    def test_raw_counts_and_hadamard_statistics(self):
        m = target()
        self.assertTrue(m["job"].result().success)
        counts = m.get("counts_dict")
        self.assertIsInstance(counts, dict, "Expose a raw counts dictionary, not the Result object")
        self.assertEqual(sum(counts.values()), 100)
        self.assertEqual(set(counts), {"0","1"})
        self.assertLess(abs(counts["1"]/100 - .5), .3)
        self.assertEqual(counts, m["job"].result().get_counts())

if __name__ == "__main__":
    unittest.main()

