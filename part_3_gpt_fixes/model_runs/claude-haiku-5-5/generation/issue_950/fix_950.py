from qiskit.quantum_info import Operator

i, j, N = 2, 8, 10
# FIX: identity was sized to j-i-1 qubits while qargs address qubits up to j-1 -> built the identity on all N qubits, because the operator must act on the full N-qubit system for the qargs to be valid
op = Operator.from_label('I' * N)
opZ = Operator.from_label('Z' * (j - i - 1))
op = op._add(opZ, qargs=list(range(i + 1, j)))
