from qiskit.quantum_info import Statevector
from qiskit.circuit.library import GroverOperator

targets = ['101', '110']

oracle = Statevector.from_label(targets)

grover_op = GroverOperator(oracle)
print(grover_op)
