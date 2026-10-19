from qiskit.quantum_info import Operator

i, j, N = 2, 8, 10
# FIX: The identity had too few qubits for qargs -> use N qubits, because the target indices belong to the full system.
op = Operator.from_label('I' * N)
opZ = Operator.from_label('Z' * (j - i - 1))
# FIX: Addition produces identity plus the Z operator -> use compose, because the desired operator applies Z only on the selected qubits.
op = op.compose(opZ, qargs=list(range(i + 1, j)))
