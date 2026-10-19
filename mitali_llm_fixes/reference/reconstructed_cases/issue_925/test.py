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
    def test_actual_shor_factors_and_simulator_capacity(self):
        m = target()
        factors = m["res"]["factors"]
        self.assertTrue(factors, "Shor must produce nontrivial factors")
        for pair in factors:
            self.assertEqual(sorted(map(int, pair)), [3,5])
        self.assertEqual(m["PRIME"], 15)
        self.assertTrue(m["backend"].configuration().simulator)
        qc = m["shor"].construct_circuit()
        self.assertEqual(qc.num_qubits, 18)
        self.assertGreaterEqual(m["backend"].configuration().n_qubits, qc.num_qubits)

if __name__ == "__main__":
    unittest.main()

