import numpy as np
from qiskit.quantum_info import Statevector
from qiskit.opflow import PrimitiveOp
from qiskit.algorithms import NumPyEigensolver

# |+>
sv = Statevector.from_label('+')
# |+><+|
proj = sv.to_operator()

# Convert to opflow operator:
op = PrimitiveOp(proj)

solver = NumPyEigensolver()
spectrum = solver.compute_eigenvalues(op)
