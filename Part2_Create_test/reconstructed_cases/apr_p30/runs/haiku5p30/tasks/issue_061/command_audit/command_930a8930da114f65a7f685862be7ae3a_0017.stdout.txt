import qiskit
from qiskit import QuantumCircuit, QuantumRegister

qr = QuantumRegister(2, 'q')
qc = QuantumCircuit(qr)
qc.h(0)
qc.cx(0, 1)

for instruction in qc.data:
    qbit: qiskit.circuit.Qubit = instruction.qubits[0]
    register = qbit._register
    # Find the index of qbit in the register
    index = None
    for i, q in enumerate(register):
        if q == qbit:
            index = i
            break
    print(register)
    print(index)
