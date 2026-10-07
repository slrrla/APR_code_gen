import numpy as np
from qiskit.quantum_info import Statevector
# FIX: only Plus was imported, but the projection needs opflow operators -> import I and X, because |+><+| = (I + X) / 2
from qiskit.opflow import Plus, I, X
from qiskit.algorithms import NumPyEigensolver

# FIX: Plus @ ~Plus composes StateFns in an unsupported order -> use the equivalent opflow operator, because |+><+| = (I + X) / 2
proj = (I + X) / 2

plus = Statevector([1/np.sqrt(2), 1/np.sqrt(2)]).to_operator()
solver = NumPyEigensolver()
# FIX: quantum_info.Operator lacks the opflow to_spmatrix API -> pass the opflow projection, because NumPyEigensolver expects an opflow operator
spectrum = solver.compute_eigenvalues(proj)

