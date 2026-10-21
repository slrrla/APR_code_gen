from qiskit.quantum_info import Operator

i, j, N = 2, 8, 10
# FIX: identity operator built on only j-i-1 qubits, so qargs 3..7 were out of range -> build it on N qubits, because qargs index into the full N-qubit register
op = Operator.from_label('I' * N)
opZ = Operator.from_label('Z' * (j - i - 1))
op = op._add(opZ, qargs=list(range(i + 1, j)))
