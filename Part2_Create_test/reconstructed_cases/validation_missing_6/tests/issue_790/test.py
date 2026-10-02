"""Synthesize evolution of the original four-qubit ZZ - XX - YY + Z model.

The answer's alternative transverse-Ising example changes the Hamiltonian and
must fail this original-question oracle. No Qiskit reference circuit is used.
"""
import contextlib
import io
import os
from pathlib import Path
import runpy
import unittest

import numpy as np
from scipy.linalg import expm
from qiskit import QuantumCircuit
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.quantum_info import Operator


CASE_DIR = Path(__file__).resolve().parent
MUT = os.environ.get("MUT", str(CASE_DIR / "fixed.py"))


def intended_terms():
    # Tensor-product matrices use the issue's four qubits, all U=J=h=t=1.
    paulis = {
        "I": np.eye(2, dtype=complex),
        "X": np.array([[0, 1], [1, 0]], dtype=complex),
        "Y": np.array([[0, -1j], [1j, 0]], dtype=complex),
        "Z": np.diag([1, -1]).astype(complex),
    }
    labels = ["ZZII", "IZZI", "IIZZ", "XXII", "IXXI", "IIXX",
              "YYII", "IYYI", "IIYY", "ZIII", "IZII", "IIZI", "IIIZ"]
    coefficients = [1, 1, 1, -1, -1, -1, -1, -1, -1, 1, 1, 1, 1]
    result = []
    for label, coefficient in zip(labels, coefficients):
        matrix = np.array([[coefficient]], dtype=complex)
        for character in label:
            matrix = np.kron(matrix, paulis[character])
        result.append(matrix)
    return result


def six_step_strang_error_bound(terms):
    """Unitary Strang local error, recursively split, telescoped over six steps.

    For A + B the bound is dt**3 * (||[A,[A,B]]||/24 +
    ||[B,[B,A]]||/12). Multiplying by six yields t**3 / 6**2.
    This permits equivalent/better synthesis without pinning circuit gates.
    """
    def commutator(left, right):
        return left @ right - right @ left

    coefficient = 0.0
    for index, left in enumerate(terms[:-1]):
        right = sum(terms[index + 1:])
        coefficient += np.linalg.norm(commutator(left, commutator(left, right)), 2) / 24
        coefficient += np.linalg.norm(commutator(right, commutator(right, left)), 2) / 12
    return coefficient / 36


class TestOriginalHamiltonianEvolution(unittest.TestCase):
    def test_hamiltonian_and_evolution(self):
        with contextlib.redirect_stdout(io.StringIO()):
            namespace = runpy.run_path(MUT)
        terms = intended_terms()
        hamiltonian = sum(terms)
        expected = expm(-1j * hamiltonian)

        # When an evolution gate is exposed, its operator must preserve the
        # requested model. Names, Pauli term order and equivalent representations
        # are immaterial; compare the full numeric matrix.
        gates = [value for value in namespace.values()
                 if isinstance(value, PauliEvolutionGate) and value.num_qubits == 4]
        if gates:
            errors = [np.linalg.norm(np.asarray(gate.operator.to_matrix()) - hamiltonian, 2)
                      for gate in gates]
            self.assertLess(min(errors), 1e-10,
                            "Hamiltonian changed: expected sum(ZZ - XX - YY) + sum(Z), U=J=h=1")

        circuits = [value for value in namespace.values()
                    if isinstance(value, QuantumCircuit) and value.num_qubits == 4]
        self.assertTrue(circuits, "synthesis must produce a four-qubit circuit")
        errors = []
        for circuit in circuits:
            actual = Operator(circuit).data
            np.testing.assert_allclose(actual.conj().T @ actual, np.eye(16), atol=1e-10)
            errors.append(np.linalg.norm(actual - expected, 2))
        bound = six_step_strang_error_bound(terms)
        self.assertGreater(bound, 0)
        self.assertLess(bound, 0.71)  # independently calculated bound: 0.7083783495
        self.assertLessEqual(min(errors), bound + 1e-10,
                             "circuit does not approximate exp(-i H) within the six-step second-order bound")


if __name__ == "__main__":
    unittest.main()
