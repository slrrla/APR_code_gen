"""Run a local job and check the real monitor's quiet interface."""
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
    def test_local_job_and_quiet_monitor(self):
        import inspect
        ns = load_target()
        monitor = ns["job_monitor"]
        self.assertTrue(callable(monitor))
        self.assertIn("quiet",inspect.signature(monitor).parameters)
        result = ns["job"].result()
        self.assertTrue(result.success)
        counts = result.get_counts()
        shots = result.results[0].shots
        self.assertEqual(sum(counts.values()),shots)
        self.assertEqual(set(counts),{"0","1"})
        self.assertAlmostEqual(counts["0"]/shots,0.5,delta=0.12)
        output = io.StringIO()
        monitor(ns["job"],quiet=True,output=output)
        self.assertEqual(output.getvalue(),"")

if __name__ == "__main__":
    unittest.main()

