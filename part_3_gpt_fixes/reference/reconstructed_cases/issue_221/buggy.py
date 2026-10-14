from qiskit import QuantumCircuit

circ = QuantumCircuit(2)
circ.h(0)
circ.cx(0, 1)

# trying to read the elements of the circuit
print(circ)
