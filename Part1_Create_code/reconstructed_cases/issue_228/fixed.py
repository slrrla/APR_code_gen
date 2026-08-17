from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
import numpy as np

op = SparsePauliOp(['X', 'Z'], [1 / np.sqrt(2), -1 / np.sqrt(2)])
print(op.is_unitary())

quantumcircuit = QuantumCircuit(2)
quantumcircuit.unitary(op, [0])

print(quantumcircuit)
