from qiskit import QuantumCircuit
output = QuantumCircuit(2)
output.h(0)
output.s(0)
output.cx(0, 1)
