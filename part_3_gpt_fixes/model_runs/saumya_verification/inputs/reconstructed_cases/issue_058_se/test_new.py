"""Intent: execute the composite Grover diffuser on the local simulator.
D = 2|s><s| - I. The implementation is allowed the global phase -1.
"""
import os
from pathlib import Path
import sys
import unittest

CASE_DIR = Path(__file__).resolve().parent
MUT = os.environ.get("MUT", str(CASE_DIR / "fixed.py"))

import numpy as np
from qiskit.quantum_info import Operator

# Resolve the shared observer even when this script runs from an isolated cwd.
sys.path.insert(0, str(CASE_DIR.parent))
from simulation_oracle import load_simulated_target


class TestIntent(unittest.TestCase):
    def test_diffuser_simulated_state_and_operator(self):
        expected = np.array([-0.75] + [0.25]*7, dtype=complex)
        ns = load_simulated_target(MUT, expected)
        for n in (2,3,4):
            dimension = 2**n
            diffusion = 2*np.ones((dimension,dimension))/dimension - np.eye(dimension)
            with self.subTest(nqubits=n):
                self.assertTrue(
                    Operator(ns["diffuser"](n)).equiv(Operator(diffusion)),
                    "The diffuser must equal 2|s><s| - I up to a global phase.",
                )

if __name__ == "__main__":
    unittest.main()
