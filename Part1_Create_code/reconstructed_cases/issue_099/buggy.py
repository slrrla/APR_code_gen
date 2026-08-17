# Attempt to build the Hamiltonians using opflow, which is deprecated
from qiskit.opflow import Z, X, I

N = 5

# H = sum_i Z_i Z_{i+1} - Z_N Z_1
hamiltonian1 = 0
for m in range(N - 1):
    term = I
    for _ in range(N - 2):
        term = term ^ I
    hamiltonian1 += Z ^ Z  # placeholder, doesn't scale properly to N qubits

hamiltonian1 += -1 * (Z ^ Z)

# H = -sum_i X_i
hamiltonian2 = 0
for m in range(N):
    hamiltonian2 += -1 * X

print(hamiltonian1)
print(hamiltonian2)
