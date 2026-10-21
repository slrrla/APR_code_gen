from qiskit import QuantumCircuit, transpile

lam = 0.5

qc = QuantumCircuit(1)
# FIX: qc.u1 was removed from QuantumCircuit in Qiskit 1.0 -> use the equivalent phase gate qc.p, because P(lam) is the same operation as U1(lam)
qc.p(lam, 0)

transpiled = transpile(qc, basis_gates=['rx', 'ry', 'rz'])
print(transpiled)
