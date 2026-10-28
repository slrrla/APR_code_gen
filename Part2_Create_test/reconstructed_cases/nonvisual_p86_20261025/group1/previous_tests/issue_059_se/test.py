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

from collections import Counter
from unittest.mock import patch
from qiskit_aer import AerSimulator

class Regression(unittest.TestCase):
    def test_marginal_counts_sum_actual_qubits_zero_and_one(self):
        run = AerSimulator.run
        def seeded(backend, *args, **kwargs):
            kwargs.setdefault("seed_simulator", 59)
            return run(backend, *args, **kwargs)
        with patch.object(AerSimulator, "run", seeded):
            m = load_target()
        expected = Counter()
        for bitstring, count in m["res"].items():
            self.assertEqual(len(bitstring), 4)
            expected[bitstring[-2:]] += count
        self.assertEqual(m["new_counts"], dict(expected))
        self.assertEqual(sum(m["new_counts"].values()), 1024)

if __name__ == "__main__":
    unittest.main()
