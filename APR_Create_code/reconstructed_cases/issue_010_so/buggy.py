from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

# Author wants to control a swap gate using quantum bits as conditions,
# analogous to c_if but with qubits instead of classical bits/registers.
qr = QuantumRegister(4, 'q')
cr = ClassicalRegister(4, 'c')
circuit = QuantumCircuit(qr, cr)

q0, q1, q2, q3 = qr

Zero = 0
One = 1

# c_if only accepts a ClassicalRegister/Clbit and an integer value,
# not a qubit -- this is the reported problem.
circuit.swap(q1, q2).c_if(q0, Zero).c_if(q3, One)
