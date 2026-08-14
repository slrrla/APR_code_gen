import numpy as np
from qiskit.circuit.library import QFT
from scipy.linalg import logm, norm
from qiskit.quantum_info import Operator

circuit = QFT(num_qubits=4, do_swaps=True)
op = Operator(circuit)
U = op.data

H = 1j * logm(U)

print(norm(U @ U.conj().T - np.identity(2**4)))  # check if U is unitary
print(norm(H - H.T.conj()))  # check if H is hermitian
