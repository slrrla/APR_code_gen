import qiskit
from qiskit import QuantumCircuit, QuantumRegister

qr = QuantumRegister(2, 'q')
qc = QuantumCircuit(qr)
qc.h(0)
qc.cx(0, 1)

for circuit_instruction in qc.data:
    qbit: qiskit.circuit.Qubit = circuit_instruction.qubits[0]
    for register, index in qc.find_bit(qbit).registers:
        print(register)
        print(index)
