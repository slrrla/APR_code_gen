"""Intent: execute the composite Grover diffuser on the local simulator.
D = 2|s><s| - I. The implementation is allowed the global phase -1.
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
    def test_diffuser_simulated_state_and_operator(self):
        ns = load_target()
        expected = np.array([-0.75] + [0.25]*7, dtype=complex)
        self.assertTrue(Statevector(ns["v"]).equiv(Statevector(expected)))
        for n in (2,3,4):
            dimension = 2**n
            diffusion = 2*np.ones((dimension,dimension))/dimension - np.eye(dimension)
            self.assertTrue(Operator(ns["diffuser"](n)).equiv(Operator(diffusion)))

if __name__ == "__main__":
    unittest.main()

