import qiskit
from qiskit import QuantumCircuit, QuantumRegister

qr = QuantumRegister(2, 'q')
qc = QuantumCircuit(qr)
qc.h(0)
qc.cx(0, 1)

for inst in qc.data:
    qbit: qiskit.circuit.Qubit = inst.qubits[0]
    loc = qc.find_bit(qbit)
    print(loc.registers[0][0])
    print(loc.registers[0][1])
