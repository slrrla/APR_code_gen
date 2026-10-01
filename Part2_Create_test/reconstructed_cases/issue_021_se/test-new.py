"""Intent: execute the custom fan-out gate and obtain the full GHZ state.
The displayed first-two-amplitudes slice is not a reduced one-qubit state;
this oracle covers the original custom-gate execution error.
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
    def test_custom_gate_execution_and_amplitudes(self):
        expected = np.zeros(8, dtype=complex)
        expected[0] = expected[7] = 1 / np.sqrt(2)
        ns = load_simulated_target(MUT, expected)
        gate = Operator(ns["cnotnot"]()).data
        for basis in range(8):
            target = basis ^ (6 if basis & 1 else 0)
            wanted = np.zeros(8)
            wanted[target] = 1
            np.testing.assert_allclose(gate[:, basis], wanted, atol=1e-12, rtol=0)

if __name__ == "__main__":
    unittest.main()
