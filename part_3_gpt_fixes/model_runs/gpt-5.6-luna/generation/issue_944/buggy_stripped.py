import numpy as np
from qiskit.quantum_info import Statevector
from qiskit.opflow import Plus
from qiskit.algorithms import NumPyEigensolver

proj = Plus @ ~Plus

plus = Statevector([1/np.sqrt(2), 1/np.sqrt(2)]).to_operator()
solver = NumPyEigensolver()
spectrum = solver.compute_eigenvalues(plus)
