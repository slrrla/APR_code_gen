import numpy as np
from qiskit.quantum_info import Statevector
from qiskit.opflow import Plus
from qiskit.opflow import MatrixOp
from qiskit.algorithms import NumPyEigensolver

# FIX: Plus @ ~Plus raises ValueError (StateFn cannot be composed first) -> use the outer product as a MatrixOp via to_density_matrix, because MatrixOp is a valid opflow operator
proj = MatrixOp(Plus.to_density_matrix())

plus = Statevector([1/np.sqrt(2), 1/np.sqrt(2)]).to_operator()
# FIX: quantum_info Operator lacks to_spmatrix needed by the solver -> wrap its matrix in an opflow MatrixOp, because MatrixOp provides the interface NumPyEigensolver expects
plus = MatrixOp(plus.data)
solver = NumPyEigensolver()
spectrum = solver.compute_eigenvalues(plus)
