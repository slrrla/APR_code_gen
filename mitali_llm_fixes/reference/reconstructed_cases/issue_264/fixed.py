from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_bloch_multivector
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from numpy import pi
import numpy as np
from qiskit.quantum_info.operators import Operator, Pauli

qreg_q = QuantumRegister(1, 'q')
circuit = QuantumCircuit(qreg_q)


# Matrix taken from
# https://docplayer.org/117986458-Die-symmetriegruppen-so-3-und-su-2.html (p. 11, equation 46)
# https://www.uni-muenster.de/Physik.TP/archive/fileadmin/lehre/teilchen/ws1011/SO3SU2.pdf (p. 8, equation 50)
def rn_su2(theta, n):
    n1 = n[0]
    n2 = n[1]
    n3 = n[2]
    return Operator([
        [np.cos(theta / 2) - 1j * n3 * np.sin(theta / 2), -1j * (n1 - 1j * n2) * np.sin(theta / 2)],
        [-1j * (n1 + 1j * n2) * np.sin(theta / 2), np.cos(theta / 2) + 1j * n3 * np.sin(theta / 2)]
    ], input_dims=(2, 1), output_dims=(2, 1))


# Magnitude of the vector n must be 1
n = [1 / np.sqrt(3), 1 / np.sqrt(3), 1 / np.sqrt(3)]

# Debug: check if the matrix is unitary
mat = np.array(rn_su2(5, n))
# Compute A^dagger.A and see if it is identity matrix
mat = np.conj(mat.T).dot(mat)
print(mat)

# construct the operator
rotated = circuit.unitary(rn_su2(pi, n), 0)
