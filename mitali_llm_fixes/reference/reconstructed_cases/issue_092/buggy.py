import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, BasicAer, transpile

qr = QuantumRegister(3)
cr = ClassicalRegister(3)

desired_vector = [0., 0.5, 0., 0.5, 0., 0.5, 0., 0.5]
qc = QuantumCircuit(qr, cr)
qc.initialize(desired_vector, qr)
backend = BasicAer.get_backend("qasm_simulator")
qc = transpile(qc, backend).inverse()

print(qc)
