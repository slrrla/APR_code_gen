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
    def test_aer_simulator_available_and_operational(self):
        m=target()
        backends=m["Aer"].backends()
        names=[b.name() if callable(b.name) else b.name for b in backends]
        self.assertIn("aer_simulator", names)
        backend=m["Aer"].get_backend("aer_simulator")
        qc=m["QuantumCircuit"](1,1)
        qc.x(0); qc.measure(0,0)
        result=backend.run(qc,shots=32).result()
        self.assertTrue(result.success)
        self.assertEqual(result.get_counts(),{"1":32})

if __name__ == "__main__":
    unittest.main()

