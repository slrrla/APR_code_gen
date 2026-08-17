from qiskit import QuantumCircuit
from numpy import pi

# 2-qubit, 2-dimensional classical data point
x = [0.5, 0.8]

qc = QuantumCircuit(2)
qc.h(0)
qc.h(1)
qc.u1(2.0 * x[0], 0)
qc.u1(2.0 * x[1], 1)

# naive (incorrect) attempt to implement exp(i*phi_{01}(x)*Z0*Z1)
# as a plain single-qubit U1 rotation -- this does NOT reproduce
# the ZZ interaction term, since Z0*Z1 is not a single-qubit operator.
qc.u1(2.0 * (pi - x[0]) * (pi - x[1]), 1)

print(qc)
