from qiskit.circuit import QuantumCircuit
from qiskit import transpile

qc = QuantumCircuit(2)
qc.h(0)
qc.s(0)
qc.cx(0, 1)

# FIX: basis lacked a way to express the 's' gate (no S = T*T rule exists in the equivalence library for this basis) -> added "s" to basis_gates, because the transpiler can then keep 's' as-is instead of failing to translate it
basis_gates = ["h", "t", "s", "cx", "id"]
qc_transpiled = transpile(qc, basis_gates=basis_gates)
