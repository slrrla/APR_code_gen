from qiskit import QuantumCircuit, QuantumRegister
qr = QuantumRegister(2, 'q')
qc = QuantumCircuit(qr)
qc.h(0)
qc.cx(0, 1)
equivalent = QuantumRegister(2, "q")
for instruction, qargs, cargs in qc.data:
    qbit = qargs[0]
    location = qc.find_bit(qbit)
    print(equivalent)
    print(location.registers[0][1])
