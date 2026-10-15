from qiskit.circuit import QuantumRegister, AncillaRegister, QuantumCircuit

qr1 = QuantumRegister(4)
anc1 = AncillaRegister(2)
qc1 = QuantumCircuit(qr1, anc1)
qc1.ccx(qr1[0], qr1[1], anc1[0])
qc1.ccx(qr1[2], anc1[0], anc1[1])
qc1.cx(anc1[1], qr1[3])
qc1.ccx(qr1[2], anc1[0], anc1[1])
qc1.ccx(qr1[0], qr1[1], anc1[0])

# FIX: circ had only 4 qubits but qc1 has 6 (4 data + 2 ancilla) -> added a 2-qubit AncillaRegister to circ, because the composed circuit must not be wider than the target
circ = QuantumCircuit(QuantumRegister(4), AncillaRegister(2))
circ.h([0, 1, 2, 3])
circ.barrier()

# FIX: qubit list mapped only 4 of qc1's 6 qubits -> map all 6 qubits including ancillas, because compose needs a target for every qubit of qc1
circ.compose(qc1, [0, 1, 2, 3, 4, 5], inplace=True)
