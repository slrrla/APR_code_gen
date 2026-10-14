import qiskit
from qiskit import QuantumCircuit, QuantumRegister

qr = QuantumRegister(2, 'q')
qc = QuantumCircuit(qr)
qc.h(0)
qc.cx(0, 1)

for instruction, qargs, cargs in qc.data:
    qbit: qiskit.circuit.Qubit = qargs[0]
    # FIX: deprecated Bit back-references -> use qc.find_bit, because it returns the register and index containing the bit
    location = qc.find_bit(qbit)
    print(location.registers[0][0])
    print(location.registers[0][1])
