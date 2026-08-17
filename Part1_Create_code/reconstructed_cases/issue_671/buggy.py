from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit

n = 4  # number of vectors to encode
v = list()  # list of register qbits to encode n vectors
a = QuantumRegister(1, "a")  # ancilla qbit
for i in range(n):
    v.append(QuantumRegister(2, "v" + str(i)))  # creates n QuantumRegister
b = ClassicalRegister(1, "b")  # classical bit

# Trying to pass a list of registers directly to QuantumCircuit - this is not supported
c = QuantumCircuit(a, v, b)
