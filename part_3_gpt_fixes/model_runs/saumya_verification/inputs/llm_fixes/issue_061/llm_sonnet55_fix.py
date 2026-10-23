import qiskit
from qiskit import QuantumCircuit, QuantumRegister

qr = QuantumRegister(2, 'q')
qc = QuantumCircuit(qr)
qc.h(0)
qc.cx(0, 1)

for instruction, qargs, cargs in qc.data:
    qbit: qiskit.circuit.Qubit = qargs[0]
    # FIX: used deprecated qbit.register and qbit.index -> look up the bit's location with qc.find_bit, because find_bit reports the containing registers and indices without the deprecated Bit back-references
    print(qc.find_bit(qbit).registers[0][0])
    print(qc.find_bit(qbit).registers[0][1])
