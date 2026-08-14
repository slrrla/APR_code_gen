from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator
import numpy as np

theta = np.pi / 4

qc = QuantumCircuit(1)
qc.rx(-np.pi / 2, 0)
qc.ry(theta, 0)
qc.rx(np.pi / 2, 0)
print(Operator(qc).data)

qc = QuantumCircuit(1)
qc.rz(theta, 0)
print(Operator(qc).data)
