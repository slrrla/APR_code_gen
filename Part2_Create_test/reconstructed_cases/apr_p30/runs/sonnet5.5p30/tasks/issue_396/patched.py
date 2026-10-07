from qiskit.quantum_info import Statevector
from qiskit.circuit.library import GroverOperator

# Desired marked (solution) states for the oracle
targets = ['101', '110']

# Indicator vector (1 on marked states, 0 elsewhere); GroverOperator uses (-1)**data
oracle = sum((Statevector.from_label(t) for t in targets[1:]), Statevector.from_label(targets[0]))

grover_op = GroverOperator(oracle)
print(grover_op)
