from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit

n = 4
v = list()
a = QuantumRegister(1, "a")
for i in range(n):
    v.append(QuantumRegister(2, "v" + str(i)))
b = ClassicalRegister(1, "b")

# FIX: passed the list v as a single argument -> unpack it with *v, because QuantumCircuit takes registers as separate positional arguments
c = QuantumCircuit(a, *v, b)
