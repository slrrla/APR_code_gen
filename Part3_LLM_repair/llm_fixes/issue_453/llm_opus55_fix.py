from qiskit.circuit import QuantumRegister, AncillaRegister, QuantumCircuit

qr1 = QuantumRegister(4)
anc1 = AncillaRegister(2)
qc1 = QuantumCircuit(qr1, anc1)
qc1.ccx(qr1[0], qr1[1], anc1[0])
qc1.ccx(qr1[2], anc1[0], anc1[1])
qc1.cx(anc1[1], qr1[3])
qc1.ccx(qr1[2], anc1[0], anc1[1])
qc1.ccx(qr1[0], qr1[1], anc1[0])

circ = QuantumCircuit(4)
circ.h([0, 1, 2, 3])
circ.barrier()

# FIX: circ had only 4 qubits but qc1 has 6 (4 data + 2 ancillas) -> add an ancilla register to circ and map qc1's ancillas onto it, because compose requires every qubit of the composed circuit to map to a qubit of the target circuit
anc = AncillaRegister(qc1.num_ancillas)
circ.add_register(anc)
circ.compose(qc1, [0, 1, 2, 3] + list(anc), inplace=True)

