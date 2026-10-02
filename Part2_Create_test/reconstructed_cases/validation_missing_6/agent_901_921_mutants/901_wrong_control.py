from qiskit import QuantumCircuit
output = QuantumCircuit(2)
output.h(0)
output.t(0)
output.t(0)
output.cx(1, 0)
