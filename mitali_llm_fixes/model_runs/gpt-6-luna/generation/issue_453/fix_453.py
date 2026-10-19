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

# FIX: circ has too few qubits for qc1 -> add two ancillas, because compose requires a target qubit for every source qubit
circ.add_register(AncillaRegister(2))
# FIX: only four target qubits were mapped for a six-qubit circuit -> map all target qubits, because qc1 uses four data qubits and two ancillas
circ.compose(qc1, circ.qubits, inplace=True)
