from qiskit.circuit import QuantumRegister, AncillaRegister, QuantumCircuit

# A subcircuit with its own ancilla qubits:
qr1 = QuantumRegister(4)
anc1 = AncillaRegister(2)
qc1 = QuantumCircuit(qr1, anc1)
qc1.ccx(qr1[0], qr1[1], anc1[0])
qc1.ccx(qr1[2], anc1[0], anc1[1])
qc1.cx(anc1[1], qr1[3])
qc1.ccx(qr1[2], anc1[0], anc1[1])
qc1.ccx(qr1[0], qr1[1], anc1[0])

# The main circuit -- has no ancillas declared, only the 4 "real" qubits
circ = QuantumCircuit(4)
circ.add_register(AncillaRegister(2))
circ.h([0, 1, 2, 3])
circ.barrier()

# Give the main circuit matching ancillas, then map all subcircuit qubits.
circ.compose(qc1, [circ.qubits[i] for i in (0, 1, 3, 2, 4, 5)], inplace=True)
