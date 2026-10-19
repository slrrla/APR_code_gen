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
    def test_printed_indices_match_actual_circuit_operands(self):
        import ast
        m = target()
        actual = [ast.literal_eval(line.split(":",1)[1].strip())
                  for line in m["_stdout"].splitlines() if line.startswith("qargs :")]
        qc = m["qc"]
        expected = [[list(qc.qubits).index(q) for q in item[1]] for item in qc.data]
        self.assertGreater(len(expected), 0)
        self.assertEqual(actual, expected)
        self.assertTrue(all(type(q) is int and 0 <= q < 3 for row in actual for q in row))

if __name__ == "__main__":
    unittest.main()

