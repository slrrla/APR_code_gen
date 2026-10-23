# FIX: Statevector was imported for an invalid list-based oracle -> import QuantumCircuit, because GroverOperator needs a circuit implementing the phase oracle
from qiskit import QuantumCircuit
from qiskit.circuit.library import GroverOperator

targets = ['101', '110']

# FIX: Statevector.from_label accepts one label and prepares a state, not an oracle -> build a diagonal phase oracle, because it flips the phase of each target basis state
oracle = QuantumCircuit(3)
oracle.diagonal([(-1 if format(i, '03b') in targets else 1) for i in range(8)], [0, 1, 2])

grover_op = GroverOperator(oracle)
print(grover_op)

