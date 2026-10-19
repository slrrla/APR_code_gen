from qiskit import QuantumRegister, QuantumCircuit
from qiskit.extensions import UnitaryGate
from qiskit.quantum_info import random_unitary

# Custom multi-qubit gate
gate = UnitaryGate(random_unitary(2 ** 4).data, 'RND-U16')

# Two separate quantum registers
qr1 = QuantumRegister(2, 'q')
qr2 = QuantumRegister(3, 'a')

circ = QuantumCircuit(qr1, qr2)

# Trying to apply the gate to qubits taken from both registers
# by passing the registers/slices separately instead of merging them
circ.append(gate, qr1[1:2], qr2[0:3])
