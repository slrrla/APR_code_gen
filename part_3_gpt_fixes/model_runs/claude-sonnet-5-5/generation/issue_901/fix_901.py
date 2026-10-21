from qiskit.circuit import QuantumCircuit
from qiskit import transpile

qc = QuantumCircuit(2)
qc.h(0)
qc.s(0)
qc.cx(0, 1)

# FIX: basis lacked a way to express 's' (no equivalence rule from {h,t,cx,id}) -> added "s" to basis_gates, because the transpiler can then keep the s gate and translation succeeds
basis_gates = ["h", "t", "s", "cx", "id"]
qc_transpiled = transpile(qc, basis_gates=basis_gates)
