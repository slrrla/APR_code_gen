from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit

n = 4
v = list()
a = QuantumRegister(1, "a")
for i in range(n):
    v.append(QuantumRegister(2, "v" + str(i)))
b = ClassicalRegister(1, "b")

# FIX: passed the list as one register argument -> unpacked the registers, because QuantumCircuit requires each register as a separate argument
c = QuantumCircuit(a, *v, b)
