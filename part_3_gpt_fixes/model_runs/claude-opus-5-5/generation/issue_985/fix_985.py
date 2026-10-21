from qiskit import QuantumCircuit, transpile

lam = 0.5

qc = QuantumCircuit(1)
# FIX: removed qc.u1 method -> use qc.p (PhaseGate, identical to U1), because u1 no longer exists and p has an rz decomposition that preserves the phase via global_phase
qc.p(lam, 0)

transpiled = transpile(qc, basis_gates=['rx', 'ry', 'rz'])
print(transpiled)
