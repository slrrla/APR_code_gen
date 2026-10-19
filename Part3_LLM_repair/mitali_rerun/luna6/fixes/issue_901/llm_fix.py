from qiskit.circuit import QuantumCircuit
from qiskit import transpile

qc = QuantumCircuit(2)
qc.h(0)
# FIX: S is not translated to T gates by this transpilation path -> express S as T², because two T gates implement S exactly
qc.t(0); qc.t(0)
qc.cx(0, 1)

basis_gates = ["h", "t", "cx", "id"]
qc_transpiled = transpile(qc, basis_gates=basis_gates)
