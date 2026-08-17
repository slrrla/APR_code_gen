from qiskit.circuit import QuantumCircuit
from qiskit.circuit.library import GroverOperator

# Desired marked (solution) states for the oracle
targets = ['101', '110']

# FIX: build the phase oracle directly as a quantum circuit using
# controlled-Z gates, which correctly flips the phase of both
# |101> and |110> states.
oracle = QuantumCircuit(3)
oracle.cz(0, 2)
oracle.cz(0, 1)

grover_op = GroverOperator(oracle)
print(grover_op)
