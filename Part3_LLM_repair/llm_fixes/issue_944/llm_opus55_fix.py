import numpy as np
from qiskit.quantum_info import Statevector
# FIX: MatrixOp was not imported -> added it to the opflow import, because it is needed to build opflow operators from matrices
from qiskit.opflow import Plus, MatrixOp
from qiskit.algorithms import NumPyEigensolver

# FIX: Plus @ ~Plus composes a StateFn as first operand (undefined) -> build the projector |+><+| as a MatrixOp from the density matrix, because opflow has no StateFn outer-product composition
proj = MatrixOp(Plus.to_density_matrix())

plus = Statevector([1/np.sqrt(2), 1/np.sqrt(2)]).to_operator()
solver = NumPyEigensolver()
# FIX: passing a quantum_info Operator (no to_spmatrix) -> wrap its matrix in MatrixOp, because NumPyEigensolver expects an opflow OperatorBase
spectrum = solver.compute_eigenvalues(MatrixOp(plus.data))
