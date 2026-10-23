from qiskit.quantum_info import Operator

i, j, N = 2, 8, 10
# Pauli labels list the highest-index qubit first.
label = 'I' * (N - j) + 'Z' * (j - i - 1) + 'I' * (i + 1)
print(label)  # <= Check!
op = Operator.from_label(label)
