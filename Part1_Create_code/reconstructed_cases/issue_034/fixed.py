from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister
from qiskit_aer import Aer

qr = QuantumRegister(1)
cr = ClassicalRegister(1)
qc = QuantumCircuit(qr, cr)
qc.h(qr[0])
qc.measure(qr, cr)

backend = Aer.get_backend('qasm_simulator')
