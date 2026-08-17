from qiskit import QuantumCircuit
from qiskit import transpile

qc = QuantumCircuit(5)
qc.cnot(0, 1)
qc.h(1)

basis = ['h', 'ccx', 'id', 'swap']
qc_basis = transpile(qc, basis_gates=basis)
print(qc_basis)
