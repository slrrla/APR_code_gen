from qiskit.quantum_info import Statevector
from qiskit.circuit.library import GroverOperator

targets = ['101', '110']

# FIX: from_label was given a list but only accepts one label string -> sum the single-label statevectors of each target, because GroverOperator builds the oracle as Diagonal((-1)**data), which flips the phase wherever the entry is 1
oracle = Statevector.from_label(targets[0]) + Statevector.from_label(targets[1])

grover_op = GroverOperator(oracle)
print(grover_op)
