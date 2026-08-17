from qiskit import QuantumCircuit

# Using integer-based initialization (no explicit registers)
circ = QuantumCircuit(7, 5)

circ.h(0)
circ.h(0).c_if(0, 3)  # c_if requires a classical register, not an int index

print(circ.draw())
