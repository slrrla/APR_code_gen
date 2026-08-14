from qiskit.circuit.library import XGate
from qiskit.quantum_info import Operator
import numpy as np

gate = XGate()

# Get the underlying array
unitary_matrix = gate.to_matrix()

# Or equivalently, using Operator
unitary_matrix = Operator(gate).data

# Now compute the eigenvalues and eigenvectors using numpy
eigenvalues, eigenvectors = np.linalg.eig(unitary_matrix)
print(eigenvalues)
# [ 1.+0.j -1.+0.j]
print(eigenvectors)
# [[ 0.70710678-0.j  0.70710678+0.j]
#  [ 0.70710678+0.j -0.70710678-0.j]]
