"""Intent: append each controlled Grover power to one control plus six fixed targets."""
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
from qiskit.quantum_info import Operator

class TestIntent(unittest.TestCase):
    def test_qpe_mapping_and_controlled_powers(self):
        ns = load_target()
        qpe = ns["qpe"]
        self.assertEqual(qpe.num_qubits, 9)
        self.assertEqual(qpe.num_clbits, 0)
        self.assertEqual(len(qpe.data), 3)
        # Analytic Grover matrix: (2|s><s| - I) Z_on_target_5.
        diffusion = np.ones((64,64))/32 - np.eye(64)
        oracle = np.diag([1]*32 + [-1]*32)
        grover = diffusion @ oracle
        for i,(op,qargs,cargs) in enumerate(qpe.data):
            self.assertEqual([qpe.qubits.index(q) for q in qargs], [i,3,4,5,6,7,8])
            self.assertFalse(cargs)
            self.assertEqual(op.num_qubits, 7)
            expected = np.zeros((128,128), dtype=complex)
            expected[::2,::2] = np.eye(64)
            expected[1::2,1::2] = np.linalg.matrix_power(grover, 2**(2-i))
            np.testing.assert_allclose(Operator(op).data, expected, atol=1e-8, rtol=0)

if __name__ == "__main__":
    unittest.main()

