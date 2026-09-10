import numpy as np
from qiskit.chemistry import FermionicOperator

def ssh_ham(gamma, lamda, n):
    sigmax = np.array([[0, 1], [1, 0]], dtype=complex)
    sigmay = np.array([[0, -1j], [1j, 0]], dtype=complex)

    identity = np.eye(n)
    cosine = 0.5 * (np.eye(n, k=1) + np.eye(n, k=-1))
    sine = 0.5j * (np.eye(n, k=1) - np.eye(n, k=-1))

    return (
        np.kron(gamma * identity + lamda * cosine, sigmax)
        + np.kron(lamda * sine, sigmay)
    )

# Correct: alternating SSH couplings gamma=1, lambda=2.
n = 10
h1 = ssh_ham(gamma=1, lamda=2, n=n)
fer_op = FermionicOperator(h1=h1)

print("Hamiltonian shape:", h1.shape)
print("Nearest-neighbor couplings:",
      [h1[i, i + 1] for i in range(2 * n - 1)])
