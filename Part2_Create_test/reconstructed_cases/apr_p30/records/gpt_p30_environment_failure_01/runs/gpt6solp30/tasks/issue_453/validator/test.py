"""Standalone behavioral regression test. MUT selects source; default: sibling fixed.py."""
import os
from pathlib import Path
import runpy
import unittest
import numpy as np

def load_target():
    return runpy.run_path(os.environ.get("MUT", str(Path(__file__).with_name("fixed.py"))), run_name="__main__")

class TestAutomaticAncillas(unittest.TestCase):
    def test_entry_point_and_clean_ancillas(self):
        from qiskit.quantum_info import Statevector
        m=load_target()
        self.assertEqual(m['circ'].num_qubits,6)
        self.assertEqual(len(m['circ'].ancillas),2)
        expected=np.zeros(64); expected[:16]=0.25
        np.testing.assert_allclose(Statevector.from_instruction(m['circ']).data,expected,atol=1e-12)

    def test_allocate_reuse_and_all_basis_inputs(self):
        from qiskit.circuit import QuantumCircuit, QuantumRegister, AncillaRegister
        from qiskit.quantum_info import Statevector
        m=load_target()
        for existing in (0,1,2,4):
            main=QuantumCircuit(QuantumRegister(4))
            if existing: main.add_register(AncillaRegister(existing))
            returned=main.compose_with_auto_ancillas(m['qc1'],[0,1,2,3],inplace=True)
            self.assertIsNone(returned)
            self.assertEqual(len(main.ancillas),max(2,existing))
            self.assertEqual(main.num_qubits,4+max(2,existing))
            for basis in range(16):
                expected=basis ^ (8 if basis & 7 == 7 else 0)
                initial=np.zeros(2**main.num_qubits); initial[basis]=1
                actual=Statevector(initial).evolve(main).data
                wanted=np.zeros_like(initial); wanted[expected]=1
                np.testing.assert_allclose(actual,wanted,atol=1e-12)
            main.compose_with_auto_ancillas(m['qc1'],[0,1,2,3],inplace=True)
            self.assertEqual(len(main.ancillas),max(2,existing))
            # Applying the clean-ancilla controlled XOR twice is identity.
            for basis in (0,7,15):
                initial=np.zeros(2**main.num_qubits); initial[basis]=1
                np.testing.assert_allclose(Statevector(initial).evolve(main).data,initial,atol=1e-12)

if __name__ == "__main__":
    unittest.main()

