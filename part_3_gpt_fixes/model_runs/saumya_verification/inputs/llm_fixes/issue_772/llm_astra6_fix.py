from qiskit import QuantumRegister, QuantumCircuit
from qiskit.extensions import UnitaryGate
from qiskit.quantum_info import random_unitary

gate = UnitaryGate(random_unitary(2 ** 4).data, 'RND-U16')

qr1 = QuantumRegister(2, 'q')
qr2 = QuantumRegister(3, 'a')

circ = QuantumCircuit(qr1, qr2)

# FIX: The second register slice was passed as classical arguments -> combine both slices as quantum arguments, because the gate requires four qubits.
circ.append(gate, qr1[1:2] + qr2[0:3])

