from qiskit.quantum_info import Statevector
from qiskit.circuit.library import GroverOperator

targets = ['101', '110']

# FIX: from_label was given a list, but it accepts only one label string -> sum the statevectors of each target label, because GroverOperator builds Diagonal((-1)**data), so entries of 1 at each target give a phase flip on all marked states
oracle = sum(Statevector.from_label(t) for t in targets[1:]) + Statevector.from_label(targets[0])

grover_op = GroverOperator(oracle)
print(grover_op)

