from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit

n = 4
v = list()
a = QuantumRegister(1, "a")
for i in range(n):
    v.append(QuantumRegister(2, "v" + str(i)))
b = ClassicalRegister(1, "b")

# FIX: passed list of registers v as a single argument -> unpacked with *v, because QuantumCircuit expects each register as a separate positional argument
c = QuantumCircuit(a, *v, b)
