from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

qreg1 = QuantumRegister(1, 'qreg1')
qreg2 = QuantumRegister(1, 'qreg2')
creg1 = ClassicalRegister(1, 'creg1')
creg2 = ClassicalRegister(1, 'creg2')

circuit = QuantumCircuit(qreg1, qreg2, creg1, creg2)
circuit.h(qreg1)
circuit.cx(qreg1, qreg2)
circuit.measure(qreg1, creg1)
circuit.measure(qreg2, creg2)

# circuit still has multiple quantum/classical registers instead of a single one
print(circuit.draw())
