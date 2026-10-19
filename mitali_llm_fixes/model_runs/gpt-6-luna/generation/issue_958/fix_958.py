from qiskit import QuantumCircuit

qc = QuantumCircuit(2)
qc.h([0, 1])

gate1 = qc.h
# FIX: A bound method cannot be multiplied by -1 -> set the circuit phase to pi, because that multiplies its unitary by -1
qc.global_phase = 3.141592653589793
