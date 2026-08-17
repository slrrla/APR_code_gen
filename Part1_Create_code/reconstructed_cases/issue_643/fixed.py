import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import UCRYGate

theta_j = np.array([np.pi / 4, np.pi / 2, 3 * np.pi / 4, np.pi])

qc = QuantumCircuit(4)
j = 0

controls = qc.qubits[j+1:]
target = [qc.qubits[j]]
qc.append(UCRYGate(theta_j.tolist()), controls + target)

print(qc)
