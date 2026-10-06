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

# The main circuit -- extend it to have the ancilla qubits needed by qc1
# qc1 needs 4 data qubits + 2 ancilla qubits = 6 total qubits
qr = QuantumRegister(4, name='q')
anc = AncillaRegister(2, name='anc')
circ = QuantumCircuit(qr, anc)
circ.h([0, 1, 2, 3])
circ.barrier()

# Now compose qc1 onto the first 4 qubits, and the 2 ancilla qubits
circ.compose(qc1, [0, 1, 2, 3, 4, 5], inplace=True)

print("Success! Circuit has {} qubits".format(circ.num_qubits))
print("Circuit depth: {}".format(circ.depth()))
print("Circuit num_clbits: {}".format(circ.num_clbits))
