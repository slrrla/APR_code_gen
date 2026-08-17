from qiskit import QuantumCircuit

qc = QuantumCircuit(3)
qc.h(0)
qc.cx(0, 1)
qc.cx(1, 2)
qc.x(2)

# Use depth() to get the actual computational cost (circuit depth)
print(qc.depth())
print(qc.count_ops())
