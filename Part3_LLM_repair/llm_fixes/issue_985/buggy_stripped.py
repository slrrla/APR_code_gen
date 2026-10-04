from qiskit import QuantumCircuit, transpile

lam = 0.5

qc = QuantumCircuit(1)
qc.u1(lam, 0)

transpiled = transpile(qc, basis_gates=['rx', 'ry', 'rz'])
print(transpiled)
