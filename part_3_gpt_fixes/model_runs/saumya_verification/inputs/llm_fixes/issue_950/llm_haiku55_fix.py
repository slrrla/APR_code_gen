from qiskit.quantum_info import Operator

i, j, N = 2, 8, 10
# FIX: op was built on j-i-1 qubits but is added with qargs range(i+1, j) on the full register -> built it on N qubits, because _add requires the base operator to span all qubits that qargs index into
op = Operator.from_label('I' * N)
opZ = Operator.from_label('Z' * (j - i - 1))
op = op._add(opZ, qargs=list(range(i + 1, j)))

