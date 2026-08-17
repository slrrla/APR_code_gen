import numpy as np

# Pauli-X matrix (also Hermitian and unitary)
X = np.array([[0, 1],
              [1, 0]])

U = X
U_dagger = X.conj().T  # for X this is the same matrix

# CORRECT: proper matrix multiplication, not elementwise sum
result = np.dot(U, U_dagger)

print("Result of U * U_dagger (matrix multiplication):")
print(result)
