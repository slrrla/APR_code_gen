from qiskit.quantum_info import Operator

i, j, N = 2, 8, 10
# FIX: identity operator was built on only j-i-1 qubits, so qargs were out of range -> build it on N qubits, because the qargs index qubits of the full N-qubit system
op = Operator.from_label('I' * N)
opZ = Operator.from_label('Z' * (j - i - 1))
op = op._add(opZ, qargs=list(range(i + 1, j)))
