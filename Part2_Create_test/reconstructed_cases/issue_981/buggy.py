import numpy as np
from qiskit.chemistry import FermionicOperator

# Incorrect: all nearest-neighbor couplings are set to 1.
n = 10
h1 = np.zeros((2 * n, 2 * n), dtype=complex)

for i in range(2 * n - 1):
    h1[i, i + 1] = 1
    h1[i + 1, i] = 1

fer_op = FermionicOperator(h1=h1)

print("Hamiltonian shape:", h1.shape)
print("Nearest-neighbor couplings:",
      [h1[i, i + 1] for i in range(2 * n - 1)])
