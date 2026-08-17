from qiskit import QuantumCircuit, execute
from qiskit import Aer
from qiskit.quantum_info import SparsePauliOp, Pauli
import numpy as np

# Create the Observable using SparsePauliOp
X = SparsePauliOp(Pauli('X'))
M_hat = X.tensor(X).tensor(X).tensor(X).tensor(X).tensor(X)
matrix_m_hat = np.real(M_hat.to_matrix())

# Circuit
psi = QuantumCircuit(6)
psi.x(0)
psi.h(1)
# No measurements or resets needed for statevector simulation

simulator = Aer.get_backend('statevector_simulator')
result = execute(psi, simulator).result()
statevector = np.array(result.get_statevector())

# Compute the expectation value
expectation = statevector.T.conj() @ matrix_m_hat @ statevector
print("expectation: ", expectation.real)
