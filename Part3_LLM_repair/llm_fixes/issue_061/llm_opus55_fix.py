import qiskit
from qiskit import QuantumCircuit, QuantumRegister

qr = QuantumRegister(2, 'q')
qc = QuantumCircuit(qr)
qc.h(0)
qc.cx(0, 1)

# FIX: tuple-unpacking CircuitInstruction is deprecated legacy behavior -> iterate instructions and use .qubits, because this is the supported attribute access
for circuit_instruction in qc.data:
    qbit: qiskit.circuit.Qubit = circuit_instruction.qubits[0]
    # FIX: deprecated/removed qbit.register and qbit.index -> qc.find_bit(qbit), because the circuit (not the Bit) now holds register/index information
    print(qc.find_bit(qbit).registers[0][0])
    print(qc.find_bit(qbit).index)

