import math
from qiskit import QuantumCircuit

qc = QuantumCircuit(1)
qc.ry(3 * math.pi / 4, 0)
