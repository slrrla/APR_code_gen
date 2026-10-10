from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit

n = 4
v = list()
a = QuantumRegister(1, "a")
for i in range(n):
    v.append(QuantumRegister(2, "v" + str(i)))
b = ClassicalRegister(1, "b")

# FIX: v was passed as a list -> unpack v, because QuantumCircuit expects individual registers.
c = QuantumCircuit(a, *v, b)

