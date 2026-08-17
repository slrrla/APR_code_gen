from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister

bob = QuantumRegister(8, "b")
alice = ClassicalRegister(2, "a")
eve = QuantumRegister(4, "e")
qc = QuantumCircuit(bob, alice, eve)

num_qubits = bob.size + alice.size + eve.size
print(num_qubits)
