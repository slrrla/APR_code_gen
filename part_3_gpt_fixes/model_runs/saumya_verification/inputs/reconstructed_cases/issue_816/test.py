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
    def test_each_shot_is_recorded_and_matches_counts(self):
        from collections import Counter
        m = target()
        memory = m["memory"]
        self.assertIsInstance(memory, list)
        self.assertEqual(len(memory), 10)
        self.assertLessEqual(set(memory), {"00", "11"})
        self.assertEqual(dict(Counter(memory)), m["result"].get_counts(m["circ"]))
        self.assertTrue(m["result"].success)

if __name__ == "__main__":
    unittest.main()

