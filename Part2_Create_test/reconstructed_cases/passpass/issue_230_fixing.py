import numpy as np
from qiskit.quantum_info import SparsePauliOp

def Hamiltonian(n, h):
    pow_n = 2**n

    pauli_terms = []

    for i in range(n-1):
        label = 'I' * (n-i-2) + 'ZZ' + 'I' * i
        pauli_terms.append((label, -1.0))

    for i in range(n):
        label = 'I' * (n-i-1) + 'X' + 'I' * i
        pauli_terms.append((label, -h))

    H = SparsePauliOp.from_list(pauli_terms)
    Hamiltonian_Matrix = H.to_matrix()

    print(f"The {pow_n} x {pow_n} Hamiltonian Matrix is:")
    print(Hamiltonian_Matrix)

    w, v = np.linalg.eigh(Hamiltonian_Matrix)
    print("Eigenvalues:", w)
    print("Eigenvectors:", v)

    min_spot = np.argmin(w)
    groundstate = v[:, min_spot]
    probability = np.square(np.abs(groundstate))
    print(f"The probability for each of the {pow_n} base states is:")
    print(probability)
    print("The probabilities add up to: %.2f" % np.sum(probability))

Hamiltonian(3, 1)
