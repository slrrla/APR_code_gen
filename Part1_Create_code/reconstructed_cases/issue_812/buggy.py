import numpy as np
from qiskit import QuantumCircuit

qc = QuantumCircuit(4)
qc.initialize(np.kron([0.8, 0.6], [1, 0]))
print(qc)
