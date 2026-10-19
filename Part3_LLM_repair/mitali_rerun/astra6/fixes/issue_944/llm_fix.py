import numpy as np
from qiskit.quantum_info import Statevector
# FIX: StateFn composition cannot construct this projector -> import MatrixOp, because it wraps matrices and quantum_info operators for opflow.
from qiskit.opflow import Plus, MatrixOp
from qiskit.algorithms import NumPyEigensolver

# FIX: Plus @ ~Plus is unsupported StateFn composition -> form the outer product in MatrixOp, because it represents |+><+| as an opflow operator.
proj = MatrixOp(np.outer(Plus.to_matrix(), Plus.to_matrix().conj()))

plus = Statevector([1/np.sqrt(2), 1/np.sqrt(2)]).to_operator()
solver = NumPyEigensolver()
# FIX: quantum_info.Operator lacks to_spmatrix -> wrap plus in MatrixOp, because NumPyEigensolver expects the opflow operator interface.
spectrum = solver.compute_eigenvalues(MatrixOp(plus))
