import numpy as np
from qiskit.quantum_info import Statevector, DensityMatrix, partial_trace

# 16 qubit system
num_qubits = 16
sv = Statevector.from_label('0' * num_qubits)

# Trace out half the qubits to get the density matrix of the remaining subsystem
qubits_to_trace = list(range(8, 16))
rho = partial_trace(sv, qubits_to_trace)

# Diagonalize the density matrix to get the pure states composing the mixture
evals, evecs = np.linalg.eigh(rho.data)

# Eigenvectors corresponding to non-zero eigenvalues are the pure states
pure_states = [
    Statevector(evecs[:, i])
    for i in range(len(evals))
    if not np.isclose(evals[i], 0)
]

# Take the dominant eigenvector as the representative pure state
statevector = pure_states[-1]
print(statevector)
