from qiskit import QuantumCircuit
from qiskit.circuit.library import XGate

# User has a unitary gate applied on a circuit and wants its eigenvectors/eigenvalues
gate = XGate()
qc = QuantumCircuit(1)
qc.append(gate, [0])

# Naive attempt: try to get eigenvectors directly from the circuit object
# (QuantumCircuit has no such method/attribute -- this is the reported problem)
eigenvalues, eigenvectors = qc.eig()
print(eigenvalues)
print(eigenvectors)
