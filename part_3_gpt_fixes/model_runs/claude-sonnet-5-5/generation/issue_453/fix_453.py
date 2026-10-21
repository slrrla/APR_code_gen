from qiskit.circuit import QuantumRegister, AncillaRegister, QuantumCircuit

qr1 = QuantumRegister(4)
anc1 = AncillaRegister(2)
qc1 = QuantumCircuit(qr1, anc1)
qc1.ccx(qr1[0], qr1[1], anc1[0])
qc1.ccx(qr1[2], anc1[0], anc1[1])
qc1.cx(anc1[1], qr1[3])
qc1.ccx(qr1[2], anc1[0], anc1[1])
qc1.ccx(qr1[0], qr1[1], anc1[0])

# FIX: circ had only 4 qubits but qc1 has 6 -> add a 2-qubit ancilla register to circ, because compose needs a target qubit for every qubit of qc1
circ = QuantumCircuit(QuantumRegister(4), AncillaRegister(2))
circ.h([0, 1, 2, 3])
circ.barrier()

# FIX: qubit list mapped only 4 of qc1's 6 qubits -> map all 6 including the ancillas, because compose requires one target per source qubit
circ.compose(qc1, [0, 1, 2, 3, 4, 5], inplace=True)
