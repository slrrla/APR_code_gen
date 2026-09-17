"""Verify register identities/order and all 512 basis mappings."""
import contextlib
import functools
import io
import os
from pathlib import Path
import runpy
import unittest
import numpy as np

MUT = os.environ.get("MUT", str(Path(__file__).with_name("fixed.py")))

@functools.lru_cache(maxsize=1)
def load_target():
    with contextlib.redirect_stdout(io.StringIO()):
        return runpy.run_path(MUT)


class TestIntent(unittest.TestCase):
    def test_registered_bits_and_full_permutation(self):
        from qiskit.quantum_info import Operator
        ns = load_target()
        circuit = ns["c"]
        self.assertEqual((circuit.num_qubits,circuit.num_clbits),(9,1))
        self.assertEqual(circuit.qregs,[ns["a"]]+ns["v"])
        self.assertEqual(circuit.cregs,[ns["b"]])
        expected_bits = list(ns["a"])+[bit for register in ns["v"] for bit in register]
        self.assertEqual(circuit.qubits,expected_bits)
        matrix = Operator(circuit).data
        expected = np.zeros((512,512),complex)
        for basis in range(512):
            output = basis ^ 2
            if basis & 8:
                output ^= 1
            expected[output,basis] = 1
        np.testing.assert_allclose(matrix,expected,atol=1e-10)

if __name__ == "__main__":
    unittest.main()

