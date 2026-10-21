from qiskit.quantum_info import Operator

i, j, N = 2, 8, 10
# FIX: base operator had only j-i-1 qubits -> use 'I' * N, because qargs range(i+1, j) refers to qubits of the full N-qubit system and must lie within the operator
op = Operator.from_label('I' * N)
opZ = Operator.from_label('Z' * (j - i - 1))
op = op._add(opZ, qargs=list(range(i + 1, j)))
