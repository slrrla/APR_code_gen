from qiskit import QuantumCircuit
from numpy import pi

# 2-qubit, 2-dimensional classical data point
x = [0.5, 0.8]

qc = QuantumCircuit(2)
qc.h(0)
qc.h(1)
qc.u1(2.0 * x[0], 0)
qc.u1(2.0 * x[1], 1)

# correct implementation of exp(i*phi_{01}(x)*Z0*Z1):
# CX * (I (x) U1(2*phi_{01})) * CX
qc.cx(0, 1)
qc.u1(2.0 * (pi - x[0]) * (pi - x[1]), 1)
qc.cx(0, 1)

print(qc)
