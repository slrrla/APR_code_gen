from qiskit import QuantumCircuit

# Build a circuit that already has some measurements on it
circuit = QuantumCircuit(3, 3)
circuit.h(0)
circuit.cx(0, 1)
circuit.measure(0, 0)
circuit.measure(1, 1)

# Now we want to add more gates and then measure all qubits,
# but we have no way of checking/removing the existing measurements first.
circuit.cx(1, 2)
circuit.measure([0, 1, 2], [0, 1, 2])

print(circuit)
