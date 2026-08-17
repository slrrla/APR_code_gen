from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

# Using explicit QuantumRegister/ClassicalRegister objects
qreg = QuantumRegister(1)
creg = ClassicalRegister(4)
circuit = QuantumCircuit(qreg, creg)

circuit.h(0).c_if(creg, 3)

print(circuit.draw())
