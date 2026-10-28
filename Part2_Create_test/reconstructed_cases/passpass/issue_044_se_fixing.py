import numpy as np
from qiskit.quantum_info import Statevector, DensityMatrix, partial_trace

num_qubits = 16
sv = Statevector.from_label('0' * num_qubits)

qubits_to_trace = list(range(8, 16))
rho = partial_trace(sv, qubits_to_trace)

if np.isclose(np.trace(rho.data @ rho.data), 1.0):
    statevector = rho.to_statevector()
    print(statevector)
else:
    evals, evecs = np.linalg.eigh(rho.data)
    statevector = Statevector(evecs[:, -1])
    print(statevector)
