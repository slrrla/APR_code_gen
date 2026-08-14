from qiskit.quantum_info import Operator

N = 3
i, j, k = 0, 1, 2

opZZ = Operator.from_label('ZZ')
opZ = Operator.from_label('Z')

op = 0 * Operator.from_label('I' * N)  # Set the initial operator to zero
op = op._add(opZZ, qargs=[i, j])
op = op._add(opZ, qargs=[k])

print(op)
