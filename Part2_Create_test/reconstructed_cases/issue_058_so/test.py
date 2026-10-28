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
    def test_one_local_job_contains_three_successful_circuit_results(self):
        m = load_target()
        result = m["job"].result()
        self.assertTrue(result.success)
        self.assertEqual(len(result.results), 3)
        for i, experiment in enumerate(result.results):
            self.assertTrue(experiment.success)
            counts = result.get_counts(i)
            self.assertEqual(set(counts), {"11"})
            self.assertEqual(sum(counts.values()), experiment.shots)
            self.assertGreater(experiment.shots, 0)

if __name__ == "__main__":
    unittest.main()
