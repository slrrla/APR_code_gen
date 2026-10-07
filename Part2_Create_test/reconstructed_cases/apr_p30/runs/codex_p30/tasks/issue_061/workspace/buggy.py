import qiskit
from qiskit import QuantumCircuit, QuantumRegister

qr = QuantumRegister(2, 'q')
qc = QuantumCircuit(qr)
qc.h(0)
qc.cx(0, 1)

for circuit_instruction in qc.data:
    instruction = circuit_instruction.operation
    qargs = circuit_instruction.qubits
    cargs = circuit_instruction.clbits
    qbit: qiskit.circuit.Qubit = qargs[0]
    bit_locations = qc.find_bit(qbit)
    print(bit_locations.index)
    print(bit_locations.registers[0])
