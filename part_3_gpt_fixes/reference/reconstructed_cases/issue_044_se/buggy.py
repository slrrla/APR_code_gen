import numpy as np
from qiskit.quantum_info import Statevector, DensityMatrix, partial_trace

# 16 qubit system
num_qubits = 16
sv = Statevector.from_label('0' * num_qubits)

# Trace out half the qubits to get the density matrix of the remaining subsystem
qubits_to_trace = list(range(8, 16))
rho = partial_trace(sv, qubits_to_trace)

# Attempt to obtain a state vector directly from the (possibly mixed) density matrix
statevector = rho.to_statevector()
print(statevector)
