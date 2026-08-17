from qiskit.quantum_info import Operator

i, j, N = 2, 8, 10
op = Operator.from_label('I' * (j - i - 1))
opZ = Operator.from_label('Z' * (j - i - 1))
op = op._add(opZ, qargs=list(range(i + 1, j)))
