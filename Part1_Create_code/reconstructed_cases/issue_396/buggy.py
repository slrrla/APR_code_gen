from qiskit.quantum_info import Statevector
from qiskit.circuit.library import GroverOperator

# Desired marked (solution) states for the oracle
targets = ['101', '110']

# BUG: Statevector.from_label only accepts a single bitstring label,
# not a list of multiple target states, so this does not build the
# intended oracle marking both |101> and |110>.
oracle = Statevector.from_label(targets)

grover_op = GroverOperator(oracle)
print(grover_op)
