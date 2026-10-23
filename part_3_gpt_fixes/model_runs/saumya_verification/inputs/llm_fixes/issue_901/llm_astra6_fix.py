from qiskit.circuit import QuantumCircuit
from qiskit import transpile
# FIX: The translator lacks an S-to-T equivalence -> import SGate, because its decomposition can be registered.
from qiskit.circuit.library import SGate

qc = QuantumCircuit(2)
qc.h(0)
qc.s(0)
qc.cx(0, 1)

basis_gates = ["h", "t", "cx", "id"]
# FIX: S cannot be translated into the requested basis -> register S = T T, because this exact equivalence enables basis translation.
s_decomposition = QuantumCircuit(1)
s_decomposition.t(0)
s_decomposition.t(0)
SGate().add_decomposition(s_decomposition)
qc_transpiled = transpile(qc, basis_gates=basis_gates)

