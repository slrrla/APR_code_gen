from qiskit.quantum_info import Statevector
from qiskit.circuit.library import GroverOperator

targets = ['101', '110']

# FIX: from_label requires one bitstring, not a list -> build a statevector supported on both targets, because GroverOperator marks its nonzero basis states
oracle = Statevector([0, 0, 0, 0, 0, 1 / 2**0.5, 1 / 2**0.5, 0])

grover_op = GroverOperator(oracle)
print(grover_op)
