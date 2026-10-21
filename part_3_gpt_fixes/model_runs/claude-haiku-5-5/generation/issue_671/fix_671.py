from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit

n = 4
v = list()
a = QuantumRegister(1, "a")
for i in range(n):
    v.append(QuantumRegister(2, "v" + str(i)))
b = ClassicalRegister(1, "b")

# FIX: passed the list `v` as a single argument, which QuantumCircuit does not accept -> unpacked it with `*v` so each register is passed separately, because QuantumCircuit takes registers as positional arguments.
c = QuantumCircuit(a, *v, b)
