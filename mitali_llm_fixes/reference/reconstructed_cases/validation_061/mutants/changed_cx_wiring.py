from qiskit import QuantumCircuit, QuantumRegister
qr = QuantumRegister(2, 'q')
qc = QuantumCircuit(qr)
qc.h(0)
qc.cx(1, 0)
for instruction, qargs, cargs in qc.data:
    qbit = qargs[0]
    location = qc.find_bit(qbit)
    print(location.index)
    print(location.registers[0])
