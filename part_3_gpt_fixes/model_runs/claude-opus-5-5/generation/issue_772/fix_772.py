from qiskit import QuantumRegister, QuantumCircuit
# FIX: qiskit.extensions was removed -> import UnitaryGate from qiskit.circuit.library, because that is its current location
from qiskit.circuit.library import UnitaryGate
from qiskit.quantum_info import random_unitary

gate = UnitaryGate(random_unitary(2 ** 4).data, 'RND-U16')

qr1 = QuantumRegister(2, 'q')
qr2 = QuantumRegister(3, 'a')

circ = QuantumCircuit(qr1, qr2)

# FIX: second register slice was passed as cargs -> concatenate both slices into one qargs list, because append(instr, qargs, cargs) needs all 4 qubits in qargs
circ.append(gate, qr1[1:2] + qr2[0:3])
