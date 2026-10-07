"""Standalone behavioral regression test. MUT selects source; default: sibling fixed.py."""
import os
from pathlib import Path
import runpy
import unittest
import numpy as np

def load_target():
    return runpy.run_path(os.environ.get("MUT", str(Path(__file__).with_name("fixed.py"))), run_name="__main__")

class TestControlledSubcircuit(unittest.TestCase):
    def test_complete_mapping_and_controlled_permutation(self):
        from qiskit.quantum_info import Statevector
        m = load_target()
        circuit = m['circ']
        self.assertEqual(circuit.num_qubits, 17)
        self.assertEqual(len(circuit.data), 1)
        instruction, qargs, _ = circuit.data[0]
        self.assertEqual(instruction.num_qubits, 17)
        self.assertEqual(list(qargs), circuit.qubits)
        # Sparse coherent input exercises active/inactive control and nonzero idle bits.
        # Independent Boolean implementation of the ten specified controlled-X gates.
        gates = [([12],4),([12,4],5),([4,12,5],6),([4,12,5,6],7),
                 ([13],5),([13,5],6),([13,5,6],7),([14],6),([14,6],7),([15],7)]
        initial = np.zeros(2**17, dtype=complex)
        rng = np.random.RandomState(917)
        indices = [0,1,2**17-2,2**17-1] + rng.choice(2**17,28,replace=False).tolist()
        for k,index in enumerate(indices):
            initial[index] += np.exp(0.37j*k)
        initial /= np.linalg.norm(initial)
        expected = np.zeros_like(initial)
        for index in np.flatnonzero(initial):
            out = int(index)
            if out & 1:
                for controls,target in gates:
                    if all((out >> (q+1)) & 1 for q in controls):
                        out ^= 1 << (target+1)
            expected[out] += initial[index]
        actual = Statevector(initial).evolve(circuit).data
        np.testing.assert_allclose(actual, expected, atol=2e-8, rtol=0)

if __name__ == "__main__":
    unittest.main()

