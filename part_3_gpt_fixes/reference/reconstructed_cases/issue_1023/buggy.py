import numpy as np
from qiskit.circuit.library import HGate
from qiskit.quantum_info import Choi, DensityMatrix, partial_trace

# Choi matrix for a Hadamard channel (process to be characterized)
choi = Choi(HGate())

# Input state: single qubit ground state |0><0|
rho_in = DensityMatrix.from_label('0')

# BUG: build (I (x) rho_in) instead of (rho_in^T (x) I), and trace out
# the wrong subsystem (system instead of ancilla), with no transpose
# and no renormalization.
rho_full = DensityMatrix(np.kron(np.eye(2), rho_in.data), dims=(2, 2))
combined = np.dot(choi.data, rho_full.data)
rho_out = partial_trace(DensityMatrix(combined, dims=(2, 2)), [0])

print(rho_out.data)
