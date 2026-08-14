from qiskit import QuantumCircuit, transpile

lam = 0.5

qc = QuantumCircuit(1)
# U1(lambda) equals Rz(lambda) up to an unobservable global phase e^{i*lambda/2}
qc.rz(lam, 0)

transpiled = transpile(qc, basis_gates=['rx', 'ry', 'rz'])
print(transpiled)
