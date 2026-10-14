import numpy as np
from qiskit.circuit.library import QFT
from scipy.linalg import norm
from qiskit.quantum_info import Operator

circuit = QFT(num_qubits=4, do_swaps=True)
op = Operator(circuit)
U = op.data

# U is unitary, so it can be diagonalized as U = V D V^-1 with |D_ii| = 1.
# Taking the branch of the logarithm directly on the eigenvalues (rather
# than using scipy.linalg.logm, whose branch choice is not guaranteed to
# give a Hermitian generator) yields a Hermitian H such that U = exp(iH).
eigvals, V = np.linalg.eig(U)
theta = np.angle(eigvals)  # log(D) = i*theta, real theta
Vinv = np.linalg.inv(V)
H = V @ np.diag(theta) @ Vinv

print(norm(U @ U.conj().T - np.identity(2**4)))  # check if U is unitary
print(norm(H - H.conj().T))  # check if H is hermitian
