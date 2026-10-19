from math import pi
from qiskit import QuantumCircuit, transpile
lam=.5
qc=QuantumCircuit(1)
qc.rz(lam+2*pi,0)
transpiled=transpile(qc,basis_gates=['rx','ry','rz'])
