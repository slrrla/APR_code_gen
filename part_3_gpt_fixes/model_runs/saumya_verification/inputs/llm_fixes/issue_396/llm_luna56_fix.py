from qiskit.quantum_info import Statevector
from qiskit.circuit.library import GroverOperator
# FIX: QuantumCircuit is required to construct a phase oracle -> import QuantumCircuit, because Statevector is not an oracle circuit
from qiskit import QuantumCircuit

targets = ['101', '110']

# FIX: Statevector.from_label accepts only one label and does not create an oracle -> use a diagonal circuit marking both targets, because their basis-state indices are 5 and 6
oracle = QuantumCircuit(3)
oracle.diagonal([1, 1, 1, 1, 1, -1, -1, 1], [0, 1, 2])

grover_op = GroverOperator(oracle)
print(grover_op)
