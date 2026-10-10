from qiskit.quantum_info import Operator

i, j, N = 2, 8, 10
# FIX: The identity covered only j-i-1 qubits -> use N qubits, because qargs refers to indices in the full system.
op = Operator.from_label('I' * N)
opZ = Operator.from_label('Z' * (j - i - 1))
# FIX: Addition produced an identity-plus-Z sum -> use composition, because the desired operator applies Z on the selected qubits and identity elsewhere.
op = op.compose(opZ, qargs=list(range(i + 1, j)))

