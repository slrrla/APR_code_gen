from qiskit import QuantumCircuit, transpile
lam=.5
qc=QuantumCircuit(1, global_phase=lam/2)
qc.rz(lam,0)
transpiled=transpile(qc,basis_gates=['rx','ry','rz'])
