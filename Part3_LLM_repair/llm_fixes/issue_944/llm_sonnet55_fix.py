import numpy as np
from qiskit.quantum_info import Statevector
from qiskit.opflow import Plus, MatrixOp
from qiskit.algorithms import NumPyEigensolver

# FIX: composing a StateFn with its adjoint using @ raises ValueError -> build the projector |+><+| as a MatrixOp from the density matrix, because a MatrixOp is a valid opflow operator
proj = MatrixOp(Plus.to_density_matrix())

plus = Statevector([1/np.sqrt(2), 1/np.sqrt(2)]).to_operator()
solver = NumPyEigensolver()
# FIX: passed a quantum_info Operator, which has no to_spmatrix -> wrap it in an opflow MatrixOp, because NumPyEigensolver expects an opflow operator
spectrum = solver.compute_eigenvalues(MatrixOp(plus))
