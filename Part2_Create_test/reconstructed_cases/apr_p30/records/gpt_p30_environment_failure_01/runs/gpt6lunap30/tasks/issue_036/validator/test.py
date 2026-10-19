"""Intent: serialize the one-qubit Hadamard circuit to OpenQASM 2.0."""
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
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator

class TestIntent(unittest.TestCase):
    def test_qasm2_round_trip(self):
        ns = load_target()
        text = ns["qasm_str"]
        self.assertIsInstance(text, str)
        self.assertTrue(text.lstrip().startswith("OPENQASM 2.0;"))
        parsed = QuantumCircuit.from_qasm_str(text)
        self.assertEqual((parsed.num_qubits, parsed.num_clbits), (1,0))
        self.assertEqual(parsed.count_ops(), {"h":1})
        np.testing.assert_allclose(Operator(parsed).data,
            np.array([[1,1],[1,-1]])/np.sqrt(2), atol=1e-12, rtol=0)

if __name__ == "__main__":
    unittest.main()

