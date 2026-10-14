from qiskit.quantum_info import Operator

i, j, N = 2, 8, 10
# FIX: The identity had too few qubits -> use N qubits, because qargs indexes the full system.
op = Operator.from_label('I' * N)
opZ = Operator.from_label('Z' * (j - i - 1))
# FIX: Addition produced identity plus Z -> compose on the target qubits, because the desired operator is Z there and identity elsewhere.
op = op.compose(opZ, qargs=list(range(i + 1, j)))
