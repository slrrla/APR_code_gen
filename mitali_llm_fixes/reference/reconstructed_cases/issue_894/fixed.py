import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator

qc = QuantumCircuit(1)
qc.rx(np.pi, 0)
qc.ry(np.pi, 0)

print('Final matrix:', np.round(Operator(qc).data, 3))
