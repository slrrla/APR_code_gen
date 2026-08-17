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

# Build the reference Clifford gate Y*(X/2) from the table (up to global phase)
ref_qc = QuantumCircuit(1)
ref_qc.rx(np.pi/2, 0)
ref_qc.y(0)

# Use Operator.equiv, which checks equivalence up to a global phase,
# instead of comparing the raw matrices element-by-element.
print('Matches Y*(X/2) table entry up to global phase:',
      Operator(qc).equiv(Operator(ref_qc)))
