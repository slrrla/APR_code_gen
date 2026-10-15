from qiskit import QuantumCircuit, transpile

lam = 0.5

qc = QuantumCircuit(1)
# FIX: qc.u1(lam, 0) used the U1 gate, which has no rule to unroll into ['rx', 'ry', 'rz'] -> replaced with rz(lam), which is in the target basis, because U1(lam) = e^{i*lam/2} * RZ(lam) and the phase is restored in the next line
qc.rz(lam, 0)
# FIX: missing global phase of U1 -> added lam/2 to global_phase, because U1(lam) = e^{i*lam/2} RZ(lam) and this keeps the phase exact
qc.global_phase += lam / 2

transpiled = transpile(qc, basis_gates=['rx', 'ry', 'rz'])
print(transpiled)
