from qiskit.quantum_info import Operator

i, j, N = 2, 8, 10
# FIX: identity built on j-i-1 qubits -> built on N qubits, because qargs up to j-1 must exist in the base operator
op = Operator.from_label('I' * N)
opZ = Operator.from_label('Z' * (j - i - 1))
# FIX: _add -> compose, because composing Z...Z onto the N-qubit identity at qargs yields Z on qubits i+1..j-1 and I elsewhere (adding would give I + Z...Z)
op = op.compose(opZ, qargs=list(range(i + 1, j)))

