from qiskit import QuantumCircuit
import math

qc = QuantumCircuit(1)
qc.ry(2 * math.pi / 4, 0)
