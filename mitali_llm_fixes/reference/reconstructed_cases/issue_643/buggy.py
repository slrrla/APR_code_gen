import numpy as np
from qiskit import QuantumCircuit

theta_j = np.array([np.pi / 4, np.pi / 2, 3 * np.pi / 4, np.pi])

qc = QuantumCircuit(4)
j = 0

# ucry was removed from QuantumCircuit in qiskit 1.x
qc.ucry(theta_j.tolist(), qc.qubits[j+1:], qc.qubits[j])

print(qc)
