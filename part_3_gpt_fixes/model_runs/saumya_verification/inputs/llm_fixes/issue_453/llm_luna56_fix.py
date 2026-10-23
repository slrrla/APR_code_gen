from qiskit.circuit import QuantumRegister, AncillaRegister, QuantumCircuit

qr1 = QuantumRegister(4)
anc1 = AncillaRegister(2)
qc1 = QuantumCircuit(qr1, anc1)
qc1.ccx(qr1[0], qr1[1], anc1[0])
qc1.ccx(qr1[2], anc1[0], anc1[1])
qc1.cx(anc1[1], qr1[3])
qc1.ccx(qr1[2], anc1[0], anc1[1])
qc1.ccx(qr1[0], qr1[1], anc1[0])

# FIX: the target had only four qubits -> allocate two additional qubits, because qc1 uses six qubits
circ = QuantumCircuit(6)
circ.h([0, 1, 2, 3])
circ.barrier()

# FIX: only four qubits were mapped -> map all six source qubits, because qc1 includes two ancillas
circ.compose(qc1, [0, 1, 2, 3, 4, 5], inplace=True)
