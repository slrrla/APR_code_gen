from qiskit import QuantumCircuit

qc = QuantumCircuit(2)
qc.h([0, 1])

# FIX: qc.h is a method, not a gate that can be multiplied by -1 -> set the circuit's global phase to pi, because this represents multiplying its unitary by -1
qc.global_phase = 3.141592653589793
