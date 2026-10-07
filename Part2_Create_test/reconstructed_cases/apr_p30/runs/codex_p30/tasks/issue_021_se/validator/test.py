"""Intent: execute the custom fan-out gate and obtain the full GHZ state.
The displayed first-two-amplitudes slice is not a reduced one-qubit state;
this oracle covers the original custom-gate execution error.
"""
import contextlib
import io
import os
from pathlib import Path
import runpy
import unittest

CASE_DIR = Path(__file__).resolve().parent
MUT = os.environ.get("MUT", str(CASE_DIR / "fixed.py"))

def load_target():
    with contextlib.redirect_stdout(io.StringIO()):
        return runpy.run_path(MUT)


import numpy as np
from qiskit.quantum_info import Operator, Statevector

class TestIntent(unittest.TestCase):
    def test_custom_gate_execution_and_amplitudes(self):
        ns = load_target()
        expected = np.zeros(8, dtype=complex)
        expected[0] = expected[7] = 1 / np.sqrt(2)
        self.assertTrue(Statevector(ns["result"]).equiv(Statevector(expected)))
        gate = Operator(ns["cnotnot"]()).data
        for basis in range(8):
            target = basis ^ (6 if basis & 1 else 0)
            wanted = np.zeros(8)
            wanted[target] = 1
            np.testing.assert_allclose(gate[:, basis], wanted, atol=1e-12, rtol=0)

if __name__ == "__main__":
    unittest.main()

