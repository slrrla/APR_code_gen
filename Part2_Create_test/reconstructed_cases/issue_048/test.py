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
    def test_controlled_s_and_t_have_exact_relative_phases(self):
        m = load_target()
        expected = np.diag([1, 1, 1, np.exp(3j*np.pi/4)])
        np.testing.assert_allclose(Operator(m["circuit"]).data, expected, atol=1e-12)

if __name__ == "__main__":
    unittest.main()
