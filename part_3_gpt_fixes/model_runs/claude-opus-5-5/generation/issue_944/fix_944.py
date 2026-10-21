import numpy as np
from qiskit.quantum_info import Statevector
# FIX: only Plus was imported -> also import MatrixOp, because it is needed to build opflow operators from matrices/Operators
from qiskit.opflow import Plus, MatrixOp
from qiskit.algorithms import NumPyEigensolver

# FIX: Plus @ ~Plus composes with a StateFn first, which is undefined -> build the projector from Plus's density matrix as a MatrixOp, because that is exactly |+><+|
proj = MatrixOp(Plus.to_density_matrix())

# FIX: a raw quantum_info Operator lacks to_spmatrix -> wrap it in MatrixOp, because NumPyEigensolver expects an opflow operator
plus = MatrixOp(Statevector([1/np.sqrt(2), 1/np.sqrt(2)]).to_operator())
solver = NumPyEigensolver()
spectrum = solver.compute_eigenvalues(plus)
