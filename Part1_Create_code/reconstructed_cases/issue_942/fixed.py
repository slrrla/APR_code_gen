from qiskit import QuantumCircuit, transpile
from qiskit.circuit.classicalfunction import BooleanExpression

# Use a higher-level construct that preserves semantic meaning
AND = BooleanExpression('x & y', name='AND')

circ = QuantumCircuit(3)
circ.append(AND, [0, 1, 2])

# Transpiling to a basis that includes ccx preserves the AND's meaning
decomposed = transpile(circ, basis_gates=["ccx"])
print(decomposed)
