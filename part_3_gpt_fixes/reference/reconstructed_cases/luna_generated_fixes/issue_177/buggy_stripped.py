from qiskit import QuantumCircuit
from qiskit.circuit.library import XGate

gate = XGate()
qc = QuantumCircuit(1)
qc.append(gate, [0])

eigenvalues, eigenvectors = qc.eig()
print(eigenvalues)
print(eigenvectors)
