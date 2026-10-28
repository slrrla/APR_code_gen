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
    def test_all_ten_compositions_accumulate_on_qubits_two_and_three(self):
        m = load_target()
        qc = m["qcom"]
        self.assertEqual((qc.num_qubits, qc.num_clbits), (8, 8))
        h = np.array([[1,1],[1,-1]], complex) / np.sqrt(2)
        crz = np.diag([1, np.exp(-1j*np.pi/4), 1, np.exp(1j*np.pi/4)])
        block = crz @ np.kron(np.eye(2), h)
        expected = np.kron(np.eye(16), np.kron(np.linalg.matrix_power(block, 10), np.eye(4)))
        np.testing.assert_allclose(Operator(qc).data, expected, atol=1e-11)

if __name__ == "__main__":
    unittest.main()
