"""Intent: a four-qubit TwoLocal ansatz accepts iSWAP entanglers on a linear chain."""
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
    def test_iswap_ansatz(self):
        ns = load_target()
        ansatz = ns["ansatz"]
        self.assertEqual(ansatz.num_qubits, 4)
        self.assertEqual(ansatz.num_parameters, 32)
        circuit = ansatz
        for _ in range(5):
            if any(op.name == "iswap" for op, _, _ in circuit.data):
                break
            circuit = circuit.decompose()
        ops = circuit.count_ops()
        self.assertEqual(ops.get("ry"), 16)
        self.assertEqual(ops.get("rz"), 16)
        self.assertEqual(ops.get("iswap"), 9)
        pairs = []
        expected = np.array([[1,0,0,0],[0,0,1j,0],[0,1j,0,0],[0,0,0,1]])
        for op, qubits, _ in circuit.data:
            if op.name == "iswap":
                pairs.append(tuple(circuit.qubits.index(q) for q in qubits))
                np.testing.assert_allclose(Operator(op).data, expected, atol=1e-12, rtol=0)
        self.assertEqual(pairs, [(0,1),(1,2),(2,3)] * 3)
        bound = ansatz.assign_parameters({p:0 for p in ansatz.parameters})
        np.testing.assert_allclose(Statevector.from_instruction(bound).probabilities(),
                                   [1] + [0]*15, atol=1e-12, rtol=0)

if __name__ == "__main__":
    unittest.main()

