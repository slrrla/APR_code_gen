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
    def test_multiple_circuits_return_separate_histograms(self):
        m = target()
        counts = m["qc"].run([0, np.pi/2, -np.pi/2])
        self.assertIsInstance(counts, list)
        self.assertEqual(len(counts), 3)
        for count in counts:
            self.assertIsInstance(count, dict)
            self.assertEqual(sum(count.values()), 100)
            self.assertLessEqual(set(count), {"0", "1"})
        self.assertEqual(counts[1], {"1": 100})
        self.assertEqual(counts[2], {"0": 100})

    def test_batch_order_and_two_qubit_outcomes(self):
        m = target()
        qc = m["QuantumCircuitWrapper"](2, m["backend"], 64)
        counts = qc.run([-np.pi/2, np.pi/2, -np.pi/2])
        self.assertEqual(counts, [{"00":64}, {"11":64}, {"00":64}])

if __name__ == "__main__":
    unittest.main()

