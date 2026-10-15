from qiskit import QuantumRegister, QuantumCircuit
# FIX: qiskit.extensions was removed in Qiskit 1.0 -> import UnitaryGate from qiskit.circuit.library, because that is its current location
from qiskit.circuit.library import UnitaryGate
from qiskit.quantum_info import random_unitary

gate = UnitaryGate(random_unitary(2 ** 4).data, 'RND-U16')

qr1 = QuantumRegister(2, 'q')
qr2 = QuantumRegister(3, 'a')

circ = QuantumCircuit(qr1, qr2)

# FIX: qr2 qubits were passed as the cargs argument -> concatenate both register slices into one qargs list, because append's third parameter is classical bits and the 4-qubit gate needs all 4 qubits in qargs
circ.append(gate, qr1[1:2] + qr2[0:3])
