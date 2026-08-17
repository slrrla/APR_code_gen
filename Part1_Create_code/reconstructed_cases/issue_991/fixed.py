from qiskit import QuantumCircuit, transpile

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc = transpile(qc, basis_gates=['cx', 'id', 'rz', 'x', 'sx'])
print(qc)
