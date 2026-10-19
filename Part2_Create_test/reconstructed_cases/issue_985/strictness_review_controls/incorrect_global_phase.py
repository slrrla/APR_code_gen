from qiskit import QuantumCircuit, transpile
qc=QuantumCircuit(1, global_phase=.5/3)
qc.rz(.5,0)
transpiled=transpile(qc,basis_gates=['rx','ry','rz'])
