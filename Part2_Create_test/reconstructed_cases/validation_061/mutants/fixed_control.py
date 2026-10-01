import qiskit
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit import Qubit

qr = QuantumRegister(2, 'q')
qc = QuantumCircuit(qr)
qc.h(0)
qc.cx(0, 1)

for instruction, qargs, cargs in qc.data:
    qbit: Qubit = qargs[0]
    bit_location = qc.find_bit(qbit)
    print(bit_location.index)
    print(bit_location.registers[0])
