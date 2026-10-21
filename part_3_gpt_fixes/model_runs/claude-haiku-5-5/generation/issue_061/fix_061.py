import qiskit
from qiskit import QuantumCircuit, QuantumRegister

qr = QuantumRegister(2, 'q')
qc = QuantumCircuit(qr)
qc.h(0)
qc.cx(0, 1)

for instruction, qargs, cargs in qc.data:
    qbit: qiskit.circuit.Qubit = qargs[0]
    # FIX: qbit.register and qbit.index used deprecated back-references from Bit to its Register -> looked up the bit's location with qc.find_bit(qbit) and printed its registers and index, because find_bit is the supported way to get this information from the circuit
    loc = qc.find_bit(qbit)
    print(loc.registers)
    print(loc.index)
