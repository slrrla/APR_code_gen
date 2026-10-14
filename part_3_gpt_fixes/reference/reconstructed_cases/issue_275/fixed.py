import numpy as np
import scipy
import h5py
from qiskit.aqua.algorithms import VQE, NumPyEigensolver
from qiskit.aqua.operators import WeightedPauliOperator, MatrixOperator, op_converter
from qiskit import Aer

backend = Aer.get_backend("qasm_simulator")

c1 = -0.5
c2 = .75
c3 = 2

n1 = 3
Hamil = np.zeros((n1, n1))
Hamil[1, 1] = c2
Hamil[2, 2] = -c3 / 2 + c2
Hamil[0, 2] = c1
Hamil[1, 2] = c1
Hamil[2, 0] = c1
Hamil[2, 1] = c1
print("(3x3) Hamiltonian")
print(Hamil)

vals, vecs = np.linalg.eig(Hamil)
print("Standard Eigenvalues: ")
print(vals)

# Fix: pad the matrix to (4x4) with a zero row/column so it can be
# represented as a sum of Pauli strings, then use MatrixOperator +
# op_converter instead of FermionicOperator.
n2 = 4
Hamil = np.zeros((n2, n2))
Hamil[1, 1] = c2
Hamil[2, 2] = -c3 / 2 + c2
Hamil[0, 2] = c1
Hamil[1, 2] = c1
Hamil[2, 0] = c1
Hamil[2, 1] = c1
print("(4x4) Hamiltonian")
print(Hamil)

Hamil_Mat = MatrixOperator(Hamil)
Hamil_Qop = op_converter.to_weighted_pauli_operator(Hamil_Mat)

q_vals = NumPyEigensolver(Hamil_Qop, k=4).run()
print("Qubit Op Eigenvalues: ")
print(q_vals['eigenvalues'])

vqe = VQE(Hamil_Qop)
vqe_result = vqe.run(backend)
print("VQE Eigenvalue: ")
print(vqe_result['eigenvalue'])
