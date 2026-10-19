from qiskit import QuantumCircuit, transpile
qc=QuantumCircuit(1)
qc.rz(-.5,0)
transpiled=transpile(qc,basis_gates=['rx','ry','rz'])
