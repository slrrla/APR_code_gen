from qiskit import QuantumCircuit

qc = QuantumCircuit(2)
qc.h([0, 1])

gate1 = qc.h
# FIX: a gate method cannot be multiplied by -1 -> add a π global phase, because H ⊗ (-H) equals -(H ⊗ H).
qc.global_phase += 3.141592653589793

