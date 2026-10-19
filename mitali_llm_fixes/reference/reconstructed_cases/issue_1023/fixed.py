import numpy as np
from qiskit.circuit.library import HGate
from qiskit.quantum_info import Choi, DensityMatrix, partial_trace

# Choi matrix for a Hadamard channel (process to be characterized)
choi = Choi(HGate())

# Input state: single qubit ground state |0><0|
rho_in = DensityMatrix.from_label('0')

# FIX: use rho_out = tr_1[ rho_C (rho_in^T (x) I) ], tracing out the
# ancilla (subsystem 1), and renormalize by the trace of the result.
rho_in_t = rho_in.data.T
rho_full = DensityMatrix(np.kron(rho_in_t, np.eye(2)), dims=(2, 2))
combined = np.dot(choi.data, rho_full.data)
rho_out = partial_trace(DensityMatrix(combined, dims=(2, 2)), [1])
rho_out = DensityMatrix(rho_out.data / np.trace(rho_out.data))

print(rho_out.data)
