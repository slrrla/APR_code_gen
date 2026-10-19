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

# FIX: circ had only four qubits and mapped only four of qc1's six -> add its ancilla register and map all six, because compose requires space and a mapping for every source qubit.
circ.add_register(anc1)
circ.compose(qc1, [0, 1, 2, 3, 4, 5], inplace=True)
