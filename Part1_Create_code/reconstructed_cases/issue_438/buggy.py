from qiskit import QuantumCircuit

qc = QuantumCircuit(3)
qc.h(0)
qc.cx(0, 1)
qc.cx(1, 2)
qc.x(2)

# Only checking gate counts, not the actual computational cost (depth)
print(qc.count_ops())
