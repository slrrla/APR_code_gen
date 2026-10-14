from qiskit import QuantumCircuit
from qiskit.circuit.library import XGate
# FIX: NumPy and Operator are needed to compute eigenvalues and eigenvectors from the circuit's matrix
import numpy as np
from qiskit.quantum_info import Operator

gate = XGate()
qc = QuantumCircuit(1)
qc.append(gate, [0])

# FIX: QuantumCircuit has no eig method -> compute the eigendecomposition of its unitary matrix
eigenvalues, eigenvectors = np.linalg.eig(Operator(qc).data)
print(eigenvalues)
print(eigenvectors)
