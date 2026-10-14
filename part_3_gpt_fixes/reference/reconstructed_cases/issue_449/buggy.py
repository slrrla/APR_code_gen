from qiskit import QuantumCircuit

qc = QuantumCircuit(3)
qc.ccx(0, 1, 2)
qc = qc.decompose()

# Only computes overall circuit depth, not T-depth specifically
depth = qc.depth()
print('depth:', depth)
