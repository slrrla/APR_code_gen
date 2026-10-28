"""Intent-based regression against unmodified MUT; defaults to sibling fixed.py."""
import contextlib
import io
import os
from pathlib import Path
import runpy
import unittest
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator, Statevector

MUT = os.environ.get("MUT", str(Path(__file__).with_name("fixed.py")))

def load_target():
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        namespace = runpy.run_path(MUT)
    namespace["_stdout"] = output.getvalue()
    return namespace

class Regression(unittest.TestCase):
    def test_more_than_one_million_shots_are_actually_returned(self):
        m = load_target()
        result = m["result"]
        self.assertTrue(result.success)
        counts = result.get_counts()
        self.assertEqual(sum(counts.values()), 1000001)
        self.assertEqual(set(counts), {"0", "1"})
        # Broad physical sanity bound, never a golden random count.
        self.assertLess(abs(counts["0"] / 1000001 - 0.5), 0.02)

if __name__ == "__main__":
    unittest.main()
