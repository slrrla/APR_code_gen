from qiskit.circuit import QuantumCircuit
from qiskit import transpile

qc = QuantumCircuit(2)
qc.h(0)
qc.s(0)
qc.cx(0, 1)

# S = T^2 so replace S with two T gates
qc2 = QuantumCircuit(2)
qc2.h(0)
qc2.t(0)
qc2.t(0)
qc2.cx(0, 1)

basis_gates = ["h", "t", "cx", "id"]
qc_transpiled = transpile(qc2, basis_gates=basis_gates)
print(qc_transpiled)
