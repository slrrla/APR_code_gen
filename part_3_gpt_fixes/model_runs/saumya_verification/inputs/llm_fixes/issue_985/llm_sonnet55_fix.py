from qiskit import QuantumCircuit, transpile

lam = 0.5

qc = QuantumCircuit(1)
# FIX: removed gate qc.u1 -> use qc.p, because u1 no longer exists and p is its equivalent, which transpiles to rz with the global phase tracked
qc.p(lam, 0)

transpiled = transpile(qc, basis_gates=['rx', 'ry', 'rz'])
print(transpiled)
