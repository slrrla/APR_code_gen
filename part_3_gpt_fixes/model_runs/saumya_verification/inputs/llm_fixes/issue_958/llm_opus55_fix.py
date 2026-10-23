from qiskit import QuantumCircuit
# FIX: missing imports for a real gate object and Operator -> added them, because scalar multiplication needs a matrix-backed object
from qiskit.circuit.library import HGate
from qiskit.quantum_info import Operator

qc = QuantumCircuit(2)
qc.h([0, 1])

# FIX: gate1 was the bound method qc.h (not a gate) -> use HGate(), because only gate objects can be converted to operators
gate1 = HGate()
# FIX: -1 * method raised TypeError and applied nothing -> build -1*Operator(gate1) and append it via qc.unitary, because this applies the negated gate to the qubit
qc.unitary(-1 * Operator(gate1), [0])

