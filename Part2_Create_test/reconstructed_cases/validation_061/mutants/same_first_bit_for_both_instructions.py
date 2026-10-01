from qiskit import QuantumCircuit, QuantumRegister
qr = QuantumRegister(2, 'q')
qc = QuantumCircuit(qr)
qc.h(0)
qc.cx(0, 1)
for instruction, qargs, cargs in qc.data:
    qbit = qc.data[0][1][0]
    location = qc.find_bit(qbit)
    print(location.index)
    print(location.registers[0])
