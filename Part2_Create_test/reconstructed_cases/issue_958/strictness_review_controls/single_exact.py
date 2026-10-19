from math import pi
from qiskit import QuantumCircuit
qc=QuantumCircuit(2, global_phase=pi)
qc.h([0,1])
