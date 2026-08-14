from qiskit import QuantumCircuit, QuantumRegister

qubit = QuantumRegister(1, 'q')
circuit = QuantumCircuit(qubit)

theta = 0.5
phi = 0.3

# Create an arbitrary one-qubit state using Ry and Rz rotations
circuit.ry(theta, qubit[0])
circuit.rz(phi, qubit[0])

# Equivalently, this could be done with a single u3 gate:
# circuit.u3(theta, phi, 0, qubit[0])

print(circuit)
