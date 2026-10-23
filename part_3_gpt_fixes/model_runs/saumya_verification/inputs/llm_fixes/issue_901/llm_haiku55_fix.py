from qiskit.circuit import QuantumCircuit
from qiskit import transpile

qc = QuantumCircuit(2)
qc.h(0)
# FIX: qc.s(0) used a gate with no translation rule into the {h, t, cx, id} basis -> replaced it with two T gates, because S = T·T exactly, so the circuit is unchanged and uses only basis gates
qc.t(0)
qc.t(0)
qc.cx(0, 1)

basis_gates = ["h", "t", "cx", "id"]
qc_transpiled = transpile(qc, basis_gates=basis_gates)
