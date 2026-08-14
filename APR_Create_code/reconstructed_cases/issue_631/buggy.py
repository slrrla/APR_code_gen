from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

qreg_q = QuantumRegister(2, 'q')
creg_c = ClassicalRegister(2, 'c')
circuit = QuantumCircuit(qreg_q, creg_c)

# Attempting to apply a Molmer-Sorensen (MS) gate directly,
# but QuantumCircuit has no such method/gate defined this way.
circuit.ms(0.27, [qreg_q[0], qreg_q[1]])

print(circuit)
