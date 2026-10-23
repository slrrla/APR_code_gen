from qiskit.circuit import QuantumCircuit
from qiskit import transpile

qc = QuantumCircuit(2)
qc.h(0)
# FIX: the S gate is not in the requested basis -> replace it with T², because S = T² exactly
qc.t(0); qc.t(0)
qc.cx(0, 1)

basis_gates = ["h", "t", "cx", "id"]
qc_transpiled = transpile(qc, basis_gates=basis_gates)

