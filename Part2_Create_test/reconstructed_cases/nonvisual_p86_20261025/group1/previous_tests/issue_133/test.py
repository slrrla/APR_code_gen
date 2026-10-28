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
    def test_modern_imports_and_real_bell_simulation(self):
        m = load_target()
        self.assertTrue(m["result"].success)
        counts = m["result"].get_counts()
        self.assertEqual(set(counts), {"00", "11"})
        self.assertEqual(sum(counts.values()), 1024)
        state = Statevector.from_instruction(m["qc"].remove_final_measurements(inplace=False))
        np.testing.assert_allclose(state.data, np.array([1,0,0,1])/np.sqrt(2), atol=1e-12)

if __name__ == "__main__":
    unittest.main()
