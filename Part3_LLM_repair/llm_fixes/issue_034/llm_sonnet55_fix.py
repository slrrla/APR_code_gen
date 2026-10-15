# FIX: imported Aer from qiskit, which no longer exports it -> import Aer from qiskit_aer and keep the other imports from qiskit, because Aer now lives in the separate qiskit-aer package
from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister
from qiskit_aer import Aer

qr = QuantumRegister(1)
cr = ClassicalRegister(1)
qc = QuantumCircuit(qr, cr)
qc.h(qr[0])
qc.measure(qr, cr)

backend = Aer.get_backend('qasm_simulator')
