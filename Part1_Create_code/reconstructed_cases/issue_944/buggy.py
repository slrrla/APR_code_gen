import numpy as np
from qiskit.quantum_info import Statevector
from qiskit.opflow import Plus
from qiskit.algorithms import NumPyEigensolver

# Attempt to build projection operator |+><+| directly in opflow
proj = Plus @ ~Plus  # ValueError: Composition with a Statefunctions in the first operand is not defined.

# Alternative attempt using quantum_info Operator directly with opflow-based solver
plus = Statevector([1/np.sqrt(2), 1/np.sqrt(2)]).to_operator()
solver = NumPyEigensolver()
spectrum = solver.compute_eigenvalues(plus)  # AttributeError: 'Operator' object has no attribute 'to_spmatrix'
