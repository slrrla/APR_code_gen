from qiskit import QuantumRegister, QuantumCircuit
from qiskit.extensions import UnitaryGate
from qiskit.quantum_info import random_unitary

gate = UnitaryGate(random_unitary(2 ** 4).data, 'RND-U16')

qr1 = QuantumRegister(2, 'q')
qr2 = QuantumRegister(3, 'a')

circ = QuantumCircuit(qr1, qr2)
circ.append(gate, qr1[1:2] + qr2[0:3])
