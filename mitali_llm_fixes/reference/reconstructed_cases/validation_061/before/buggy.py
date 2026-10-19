import qiskit
from qiskit import QuantumCircuit, QuantumRegister

qr = QuantumRegister(2, 'q')
qc = QuantumCircuit(qr)
qc.h(0)
qc.cx(0, 1)

for instruction, qargs, cargs in qc.data:
    qbit: qiskit.circuit.Qubit = qargs[0]
    print(qbit.register)
    print(qbit.index)
