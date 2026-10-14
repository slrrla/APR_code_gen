from qiskit import QuantumCircuit, QuantumRegister

qubit = QuantumRegister(1, 'q')
circuit = QuantumCircuit(qubit)

# Trying to create a qubit in an arbitrary state
# Attempted to use "Arbitrary Initialization" but it's not accessible (404 error)
theta = 0.5
phi = 0.3

# No initialization applied - qubit remains in |0> state
print(circuit)
