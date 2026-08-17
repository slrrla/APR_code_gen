from qiskit import QuantumCircuit
from qiskit.quantum_info import DensityMatrix, partial_trace

qc = QuantumCircuit(3)
qc.h(0)
qc.cx(0, 1)
qc.cx(0, 2)

rho = DensityMatrix(qc)
rho_a = partial_trace(state=rho, qargs=[1, 2])
print(rho_a)
