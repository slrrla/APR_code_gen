"""Standalone behavioral regression test. MUT selects source; default: sibling fixed.py."""
import os
from pathlib import Path
import runpy
import unittest
import numpy as np

def load_target():
    return runpy.run_path(os.environ.get("MUT", str(Path(__file__).with_name("fixed.py"))), run_name="__main__")

class TestRegisterQargs(unittest.TestCase):
    def test_flattened_order_and_complete_circuit_operator(self):
        from qiskit.quantum_info import Operator
        m=load_target()
        circuit=m['circ']
        instruction,qargs,_=circuit.data[-1]
        # Use the register roles assigned by the supplied snippet, including its naming swap.
        expected_qargs=list(m['train_register'])+list(m['control'])
        self.assertEqual(list(qargs),expected_qargs)
        self.assertEqual(len(qargs),4)
        self.assertEqual(len(set(qargs)),4)
        self.assertEqual(instruction.num_qubits,4)
        h=np.array([[1,1],[1,-1]])/np.sqrt(2)
        x=np.array([[0,1],[1,0]])
        # Physical qubits 0..2 get H; oracle's last argument is physical qubit 2.
        expected=np.kron(np.eye(2),np.kron(x@h,np.kron(h,h)))
        np.testing.assert_allclose(Operator(circuit).data,expected,atol=1e-12)

if __name__ == "__main__":
    unittest.main()

