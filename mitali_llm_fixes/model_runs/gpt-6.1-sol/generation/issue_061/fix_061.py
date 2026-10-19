import qiskit
from qiskit import QuantumCircuit, QuantumRegister

qr = QuantumRegister(2, 'q')
qc = QuantumCircuit(qr)
qc.h(0)
qc.cx(0, 1)

for instruction, qargs, cargs in qc.data:
    qbit: qiskit.circuit.Qubit = qargs[0]
    # FIX: deprecated Bit back-references -> use circuit lookup, because it provides the containing register and register-local index without warnings
    print(qc.find_bit(qbit).registers[0][0])
    print(qc.find_bit(qbit).registers[0][1])
