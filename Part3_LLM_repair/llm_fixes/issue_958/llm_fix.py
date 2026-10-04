from qiskit import QuantumCircuit

qc = QuantumCircuit(2)
qc.h([0, 1])

gate1 = qc.h
# FIX: scalar multiplication cannot negate a circuit method -> apply the gate inverse, because Qiskit gates use inverse() instead of arithmetic negation
gate1([0, 1]).inverse()
