from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit

n = 4  # number of vectors to encode
v = list()  # list of register qbits to encode n vectors
a = QuantumRegister(1, "a")  # ancilla qbit
for i in range(n):
    v.append(QuantumRegister(2, "v" + str(i)))  # creates n QuantumRegister
b = ClassicalRegister(1, "b")  # classical bit

c = QuantumCircuit(a, b)

# Use add_register to add each register in the list one by one
for reg in v:
    c.add_register(reg)

c.x(v[0][0])
c.cx(v[1][0], a[0])
