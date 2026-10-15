import numpy as np
from qiskit.quantum_info import Statevector
from qiskit.opflow import Plus, MatrixOp
from qiskit.algorithms import NumPyEigensolver

# FIX: Plus @ ~Plus composes two state functions, which opflow rejects -> build the |+><+| projector matrix as an opflow MatrixOp, because MatrixOp is an opflow operator that NumPyEigensolver accepts
proj = MatrixOp(Statevector([1/np.sqrt(2), 1/np.sqrt(2)]).to_operator().data)

plus = Statevector([1/np.sqrt(2), 1/np.sqrt(2)]).to_operator()
solver = NumPyEigensolver()
# FIX: solver was given the quantum_info Operator (no to_spmatrix) -> pass the opflow projector proj instead, because the eigensolver needs an opflow operator and the spectrum of the projector is what was wanted
spectrum = solver.compute_eigenvalues(proj)
