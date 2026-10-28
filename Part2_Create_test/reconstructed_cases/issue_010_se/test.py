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

from unittest.mock import patch

class Regression(unittest.TestCase):
    def test_results_retain_submission_order_under_reverse_completion(self):
        # Control only the scheduler's legal completion order; every worker runs.
        def reverse_completion(futures):
            return iter(sorted(list(futures), key=lambda f: f.result()["name"], reverse=True))
        with patch("concurrent.futures.as_completed", reverse_completion):
            m = load_target()
        self.assertEqual([r["name"] for r in m["results"]],
                         ["circuit_0", "circuit_1", "circuit_2", "circuit_3"])
        self.assertEqual(m["_stdout"].strip().splitlines(),
                         ["circuit_0 circuit_0", "circuit_1 circuit_1",
                          "circuit_2 circuit_2", "circuit_3 circuit_3"])

if __name__ == "__main__":
    unittest.main()
