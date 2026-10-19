from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_bloch_multivector
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from numpy import pi
import numpy as np
from qiskit.quantum_info.operators import Operator, Pauli

qreg_q = QuantumRegister(1, 'q')
circuit = QuantumCircuit(qreg_q)


def rn_su2_5(theta, n1, n2, n3):
    # This represents a matrix operator that will evolve() a Statevector by
    # matrix-vector multiplication and will evolve() a DensityMatrix by
    # left and right multiplication
    return Operator([
        [np.cos(theta / 2) - 1j * n3 * np.sin(theta / 2), -1j * (n1 - 1j * n2) * np.sin(theta / 2)],
        [-1j * (n1 + 1j * n2) * np.sin(theta / 2), np.cos(theta / 2) + 1j * n3 * np.sin(theta / 2)]
    ], input_dims=(2, 1), output_dims=(2, 1))


print(rn_su2_5(pi, 1, 1, 1))
# n = [1,1,1] is not a unit vector, so the resulting matrix is not unitary
circuit.unitary(rn_su2_5(pi, 1, 1, 1), 0)
