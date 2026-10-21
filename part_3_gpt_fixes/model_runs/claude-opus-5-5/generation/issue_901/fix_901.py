from qiskit.circuit import QuantumCircuit
from qiskit import transpile
# FIX: no equivalence rule maps S into {h, t, cx} -> import SGate and SessionEquivalenceLibrary, because we need to register S = T·T
from qiskit.circuit.library import SGate
from qiskit.circuit.equivalence_library import SessionEquivalenceLibrary

qc = QuantumCircuit(2)
qc.h(0)
qc.s(0)
qc.cx(0, 1)

# FIX: BasisTranslator had no path from 's' to the target basis -> add the exact equivalence S = T·T to the session library, because transpile uses SessionEquivalenceLibrary by default
s_equiv = QuantumCircuit(1)
s_equiv.t(0)
s_equiv.t(0)
SessionEquivalenceLibrary.add_equivalence(SGate(), s_equiv)

basis_gates = ["h", "t", "cx", "id"]
qc_transpiled = transpile(qc, basis_gates=basis_gates)
