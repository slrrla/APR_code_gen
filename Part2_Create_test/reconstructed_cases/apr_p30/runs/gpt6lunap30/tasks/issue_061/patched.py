import qiskit
from qiskit import QuantumCircuit, QuantumRegister

qr = QuantumRegister(2, 'q')
qc = QuantumCircuit(qr)
qc.h(0)
qc.cx(0, 1)

for circuit_instruction in qc.data:
    qbit: qiskit.circuit.Qubit = circuit_instruction.qubits[0]
    register, index = qc.find_bit(qbit).registers[0]
    print(register)
    print(index)
