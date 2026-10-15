from qiskit.circuit import QuantumRegister, AncillaRegister, QuantumCircuit

qr1 = QuantumRegister(4)
anc1 = AncillaRegister(2)
qc1 = QuantumCircuit(qr1, anc1)
qc1.ccx(qr1[0], qr1[1], anc1[0])
qc1.ccx(qr1[2], anc1[0], anc1[1])
qc1.cx(anc1[1], qr1[3])
qc1.ccx(qr1[2], anc1[0], anc1[1])
qc1.ccx(qr1[0], qr1[1], anc1[0])

# FIX: circ had only 4 qubits but qc1 has 4 data + 2 ancilla qubits -> widened circ to 4 + anc1.size, because compose needs the target to hold every qubit of the subcircuit
circ = QuantumCircuit(4 + anc1.size)
circ.h([0, 1, 2, 3])
circ.barrier()

# FIX: qubit map only covered 4 qubits -> mapped all 6 qubits of qc1 onto circ's 6 qubits, because compose requires one target qubit per subcircuit qubit
circ.compose(qc1, [0, 1, 2, 3, 4, 5], inplace=True)
