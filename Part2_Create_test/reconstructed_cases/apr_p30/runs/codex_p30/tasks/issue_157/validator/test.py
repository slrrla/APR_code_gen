"""Intent: replace reset-based initialization with controlled state preparation.
The reconstructed caller requests TWO controls via control(2). The supplied
fixed example uses control() (one control), which is reported as a contract
mismatch rather than making the test adopt the changed interface.
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

def produced_gate(ns):
    gate = ns.get("controlled_gate", ns.get("gate"))
    if gate is None:
        raise AssertionError("No controlled preparation gate was produced")
    return gate

class TestIntent(unittest.TestCase):
    def test_controlled_preparation_semantics(self):
        gate = produced_gate(load_target())
        controls = gate.num_ctrl_qubits
        self.assertGreaterEqual(controls, 1)
        self.assertEqual(gate.num_qubits - controls, 2)
        matrix = Operator(gate).data
        mask = (1 << controls) - 1
        self.assertEqual(gate.ctrl_state, mask)
        expected = np.zeros(2**gate.num_qubits, dtype=complex)
        expected[[mask + (target << controls) for target in range(4)]] = 0.5
        # State preparation specifies a state up to global phase. Older isometry
        # synthesis can choose a different phase for the prepared state.
        self.assertTrue(Statevector(matrix[:,mask]).equiv(Statevector(expected)))
        for target in range(4):
            for control in range(mask):
                basis = (target << controls) + control
                inactive = np.zeros(2**gate.num_qubits, dtype=complex)
                inactive[basis] = 1
                np.testing.assert_allclose(matrix[:,basis], inactive, atol=1e-9, rtol=0)

    def test_preserves_requested_two_controls(self):
        gate = produced_gate(load_target())
        self.assertEqual(gate.num_ctrl_qubits, 2,
                         "Caller requested control(2); a one-control replacement changes the interface")
        self.assertEqual(gate.num_qubits, 4)

if __name__ == "__main__":
    unittest.main()
