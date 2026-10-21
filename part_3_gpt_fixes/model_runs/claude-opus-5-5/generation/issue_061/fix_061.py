import qiskit
from qiskit import QuantumCircuit, QuantumRegister

qr = QuantumRegister(2, 'q')
qc = QuantumCircuit(qr)
qc.h(0)
qc.cx(0, 1)

# FIX: legacy tuple unpacking of CircuitInstruction is deprecated -> iterate instructions and use .qubits, because CircuitInstruction exposes qubits as an attribute
for instruction in qc.data:
    qbit: qiskit.circuit.Qubit = instruction.qubits[0]
    # FIX: Bit.register/Bit.index back-references are deprecated/removed -> use qc.find_bit(qbit).registers, because the circuit maps each bit to its (register, index) pairs
    print(qc.find_bit(qbit).registers[0][0])
    print(qc.find_bit(qbit).registers[0][1])
