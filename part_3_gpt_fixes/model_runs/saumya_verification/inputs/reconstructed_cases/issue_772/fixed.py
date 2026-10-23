from qiskit import QuantumRegister, QuantumCircuit
from qiskit.extensions import UnitaryGate
from qiskit.quantum_info import random_unitary

# Custom multi-qubit gate
gate = UnitaryGate(random_unitary(2 ** 4).data, 'RND-U16')

# Two separate quantum registers
qr1 = QuantumRegister(2, 'q')
qr2 = QuantumRegister(3, 'a')

circ = QuantumCircuit(qr1, qr2)

# Merge the qubit lists from both registers using "+"
circ.mct(qr1[0:2] + qr2[0:2], qr2[2])
circ.append(gate, qr1[1:2] + qr2[0:3])
