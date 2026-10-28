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
    def test_actual_aer_result_exposes_saved_bell_statevector(self):
        m = load_target()
        result = m["psi_out_complex"]
        self.assertTrue(result.success)
        state = np.asarray(result.get_statevector(), complex)
        np.testing.assert_allclose(state, np.array([1,0,0,1])/np.sqrt(2), atol=1e-12)

if __name__ == "__main__":
    unittest.main()
