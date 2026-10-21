from qiskit import QuantumRegister, QuantumCircuit
from qiskit.extensions import UnitaryGate
from qiskit.quantum_info import random_unitary

gate = UnitaryGate(random_unitary(2 ** 4).data, 'RND-U16')

qr1 = QuantumRegister(2, 'q')
qr2 = QuantumRegister(3, 'a')

circ = QuantumCircuit(qr1, qr2)

# FIX: qubits passed as two separate arguments (second treated as clbits) -> concatenated into a single qargs list, because append expects one qubit list for the 4-qubit gate
circ.append(gate, qr1[1:2] + qr2[0:3])
