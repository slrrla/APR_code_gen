from qiskit import QuantumCircuit, transpile

lam = 0.5

qc = QuantumCircuit(1)
# FIX: QuantumCircuit.u1 was removed in Qiskit 1.0 -> use qc.p, because PhaseGate is the identical replacement for U1 and has a decomposition rule into rx/ry/rz
qc.p(lam, 0)

transpiled = transpile(qc, basis_gates=['rx', 'ry', 'rz'])
print(transpiled)
