from qiskit import QuantumRegister, QuantumCircuit
from qiskit.extensions import UnitaryGate
from qiskit.quantum_info import random_unitary

gate = UnitaryGate(random_unitary(2 ** 4).data, 'RND-U16')

qr1 = QuantumRegister(2, 'q')
qr2 = QuantumRegister(3, 'a')

circ = QuantumCircuit(qr1, qr2)

# FIX: qubits from the second register were passed as cargs (classical bits) -> combined both qubit slices into a single qargs list, because append's second argument is the qubit list the gate acts on
circ.append(gate, qr1[1:2] + qr2[0:3])
