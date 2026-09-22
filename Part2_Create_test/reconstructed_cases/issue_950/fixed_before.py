from qiskit.quantum_info import Operator

i, j, N = 2, 8, 10
label = 'I' * (i + 1) + 'Z' * (j - i - 1) + 'I' * (N - j)
print(label)  # <= Check!
op = Operator.from_label(label)
