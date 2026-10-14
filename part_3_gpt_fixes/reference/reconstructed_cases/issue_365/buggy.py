import numpy as np
from qiskit import QuantumCircuit

# Minimal reproduction of the removed QuantumCircuit.uc method (qiskit 1.1)
n = 3
qc = QuantumCircuit(n)

# A simple single-qubit unitary to apply as a uniformly controlled gate
U_0 = np.array([[1, 0], [0, 1]])

j = 0
qc.uc(U_0, qc.qubits[j+1:], qc.qubits[j], up_to_diagonal=True)

print(qc)
