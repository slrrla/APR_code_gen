from qiskit import QuantumCircuit

circuit1 = QuantumCircuit(5)
circuit1.mcx([0, 1, 3, 4], 2)
print(circuit1)

circuit2 = QuantumCircuit(2)
circuit2.cx(0, 1)
print(circuit2)

# Compose circuits of different sizes by explicitly specifying
# which qubits of circuit1 map to circuit2's qubits.
circuit = circuit1.compose(circuit2, qubits=[3, 2])
print(circuit)
