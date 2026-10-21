from qiskit import QuantumCircuit, transpile

lam = 0.5

qc = QuantumCircuit(1)
# FIX: u1 gate was removed from Qiskit -> use the equivalent p gate, because p(lam) is the same operation as u1(lam) and can be translated to rz with a tracked global phase
qc.p(lam, 0)

transpiled = transpile(qc, basis_gates=['rx', 'ry', 'rz'])
print(transpiled)
