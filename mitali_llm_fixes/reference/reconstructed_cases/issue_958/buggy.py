from qiskit import QuantumCircuit

qc = QuantumCircuit(2)
qc.h([0, 1])

# Attempting to apply the negative of a gate directly - not valid Qiskit syntax
gate1 = qc.h
-1 * gate1
