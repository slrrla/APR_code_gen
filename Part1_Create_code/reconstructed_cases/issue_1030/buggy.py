import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator

qc = QuantumCircuit(1)
qc.rx(-np.pi/2, 0)
qc.rx(np.pi, 0)
qc.rx(-np.pi/2, 0)
qc.ry(np.pi/2, 0)
qc.rx(np.pi/2, 0)   # 4th
qc.rx(-np.pi/2, 0)
qc.ry(np.pi/2, 0)
qc.rx(-np.pi/2, 0)

print('Final matrix:', Operator(qc).data)

# Naively compare the resulting matrix directly against the X/2 table entry,
# ignoring the possibility of a global phase difference.
reference_X_half = np.array([[1, -1j], [-1j, 1]]) / np.sqrt(2)  # X/2 from the table
print('Matches X/2 table entry:', np.allclose(Operator(qc).data, reference_X_half))
