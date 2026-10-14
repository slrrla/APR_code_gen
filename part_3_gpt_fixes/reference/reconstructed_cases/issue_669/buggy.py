from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
import numpy as np

# prepare a simple statevector to initialize with
psi = np.array([1, 0, 0, 1]) / np.sqrt(2)

qc = QuantumCircuit(2)
qc.initialize(psi, [0, 1])

qc2 = qc
for d in range(20):
    qc2 = qc2.decompose()

# only get the final statevector, no intermediate states possible
Statevector.from_instruction(qc2)
