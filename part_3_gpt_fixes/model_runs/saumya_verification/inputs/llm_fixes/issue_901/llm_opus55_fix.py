from qiskit.circuit import QuantumCircuit
from qiskit import transpile
# FIX: equivalence library had no rule expressing S in {h, t, cx} -> import tools to add one, because BasisTranslator only uses known equivalences
from qiskit.circuit.equivalence_library import SessionEquivalenceLibrary
from qiskit.circuit.library import SGate

qc = QuantumCircuit(2)
qc.h(0)
qc.s(0)
qc.cx(0, 1)

# FIX: missing S -> T·T equivalence -> register it in the session library, because S = T^2 exactly and lets the translator reach the target basis
_s_eq = QuantumCircuit(1)
_s_eq.t(0)
_s_eq.t(0)
SessionEquivalenceLibrary.add_equivalence(SGate(), _s_eq)

basis_gates = ["h", "t", "cx", "id"]
qc_transpiled = transpile(qc, basis_gates=basis_gates)

