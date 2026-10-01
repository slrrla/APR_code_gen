from qiskit import QuantumCircuit, QuantumRegister
qr = QuantumRegister(2, 'q')
qc = QuantumCircuit(qr)
qc.h(0)
qc.cx(0, 1)
for instruction, qargs, cargs in qc.data:
    qbit = qargs[0]
    print(getattr(qbit, "_register"))
    print(getattr(qbit, "_index"))
