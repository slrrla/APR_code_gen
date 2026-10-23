"""Composition behavior, accepting preallocated or automatic workspace.

MUT selects source; default: sibling fixed.py. The question's accepted answer
offers both approaches, so a particular monkey-patched helper is not required.
"""
import os
from pathlib import Path
import runpy
import unittest
import numpy as np

def load_target():
    return runpy.run_path(os.environ.get("MUT", str(Path(__file__).with_name("fixed.py"))), run_name="__main__")

class TestAncillaComposition(unittest.TestCase):
    def test_entry_point_and_clean_workspace(self):
        from qiskit.quantum_info import Statevector
        circuit=load_target()['circ']
        # Extra preallocated workspace and ordinary QuantumRegisters are valid.
        self.assertGreaterEqual(circuit.num_qubits,6)
        expected=np.zeros(2**circuit.num_qubits); expected[:16]=0.25
        self.assertTrue(Statevector.from_instruction(circuit).equiv(expected),
                        'The prepared data superposition must retain zeroed workspace')

    def test_composed_subroutine_on_all_basis_inputs(self):
        from qiskit.circuit import QuantumCircuit
        from qiskit.quantum_info import Statevector
        circuit=load_target()['circ']
        self.assertGreaterEqual(circuit.num_qubits,6)
        # Cancel the example's input Hadamards. The uniform superposition alone
        # would incorrectly accept an omitted controlled XOR.
        logical=QuantumCircuit(circuit.num_qubits)
        logical.h([0,1,2,3])
        logical.compose(circuit,inplace=True)
        for basis in range(16):
            with self.subTest(basis=basis):
                expected_basis=basis ^ (8 if basis & 7 == 7 else 0)
                initial=np.zeros(2**circuit.num_qubits); initial[basis]=1
                expected=np.zeros_like(initial); expected[expected_basis]=1
                self.assertTrue(Statevector(initial).evolve(logical).equiv(expected),
                                'Composition must implement the data XOR and clean its workspace')

if __name__ == "__main__":
    unittest.main()

