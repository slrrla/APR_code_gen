import numpy as np

# Pauli-X matrix (also Hermitian and unitary)
X = np.array([[0, 1],
              [1, 0]])

# The user tried to verify U * U_dagger = I by doing an elementwise
# "inner product" (summing all elementwise products) instead of a
# proper matrix multiplication. This reproduces that mistake.
U = X
U_dagger = X.conj().T  # for X this is the same matrix

# WRONG: elementwise multiply and sum everything into a single scalar
result = np.sum(U * U_dagger)

print("Result of (incorrect) elementwise inner product:")
print(result)
