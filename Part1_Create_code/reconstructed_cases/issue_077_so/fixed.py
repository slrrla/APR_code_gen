from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from numpy import pi

qreg_q = QuantumRegister(3, 'q')
creg_c = ClassicalRegister(2, 'c')
circuit = QuantumCircuit(qreg_q, creg_c)

# Set the input bits A and B (00 + 01 = 01)
circuit.x(qreg_q[0])  # Set A to 1
circuit.x(qreg_q[1])  # Set B to 1

# Perform addition
circuit.ccx(qreg_q[0], qreg_q[1], qreg_q[2])  # Controlled-X gate for the sum
circuit.cx(qreg_q[0], qreg_q[1])  # Carry

# Measure the result
circuit.measure(qreg_q[1], creg_c[0])  # Result bit
circuit.measure(qreg_q[2], creg_c[1])  # Carry bit
