import numpy as np
from qiskit import QuantumCircuit
from qiskit.extensions import Initialize

qc = QuantumCircuit(4)
init_gate = Initialize([0.8, 0.6])
qc.append(init_gate, [0])
print(qc)
