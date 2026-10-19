from qiskit import Aer, ClassicalRegister, QuantumCircuit, QuantumRegister

qr = QuantumRegister(1)
cr = ClassicalRegister(1)
qc = QuantumCircuit(qr, cr)
qc.h(qr[0])
qc.measure(qr, cr)

backend = Aer.get_backend('qasm_simulator')
