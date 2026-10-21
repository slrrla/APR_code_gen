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

# FIX: circ had only 4 qubits and qc1's 2 ancillas were unmapped -> add an ancilla register to circ and map all 6 qubits, because compose requires the other circuit to be no wider than the target and every qubit to be mapped
anc2 = AncillaRegister(2)
circ.add_register(anc2)
circ.compose(qc1, circ.qubits[:4] + list(anc2), inplace=True)
