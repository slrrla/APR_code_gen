from qiskit import QuantumCircuit

circuit1 = QuantumCircuit(5)
circuit1.mcx([0, 1, 3, 4], 2)
print(circuit1)

circuit2 = QuantumCircuit(2)
circuit2.cx(0, 1)
print(circuit2)

# Attempting to combine two circuits of different sizes/qubit mappings
# using simple addition/compose without specifying qubit wiring.
circuit = circuit1 + circuit2
print(circuit)
