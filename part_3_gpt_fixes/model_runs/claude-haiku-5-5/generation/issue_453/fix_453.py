from qiskit.circuit import QuantumRegister, AncillaRegister, QuantumCircuit

qr1 = QuantumRegister(4)
anc1 = AncillaRegister(2)
qc1 = QuantumCircuit(qr1, anc1)
qc1.ccx(qr1[0], qr1[1], anc1[0])
qc1.ccx(qr1[2], anc1[0], anc1[1])
qc1.cx(anc1[1], qr1[3])
qc1.ccx(qr1[2], anc1[0], anc1[1])
qc1.ccx(qr1[0], qr1[1], anc1[0])

# FIX: circ had only 4 qubits but qc1 has 6 (4 data + 2 ancilla) -> widened circ to 6 qubits, because compose needs a target wire for every qubit of the subcircuit
circ = QuantumCircuit(6)
circ.h([0, 1, 2, 3])
circ.barrier()

# FIX: mapping list only covered 4 wires -> map all 6 wires [0..5] so the ancillas of qc1 land on circ's extra qubits, because compose requires a one-to-one mapping of every subcircuit qubit
circ.compose(qc1, [0, 1, 2, 3, 4, 5], inplace=True)
