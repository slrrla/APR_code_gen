from qiskit import *
import numpy as np

qc = QuantumCircuit(1)
theta = 0.5 * np.pi
qc.ry(np.pi / 2, 0)
qc.rx(-np.pi / 2, 0)
qc.ry(theta, 0)
qc.rx(np.pi / 2, 0)
qc.ry(-np.pi / 2, 0)

print(qc)
