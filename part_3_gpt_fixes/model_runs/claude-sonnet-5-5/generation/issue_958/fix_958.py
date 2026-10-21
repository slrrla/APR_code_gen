from qiskit import QuantumCircuit
from math import pi

qc = QuantumCircuit(2)
qc.h([0, 1])

# FIX: gate1 was a bound method (qc.h) and `-1 * gate1` is invalid -> build the gate from a circuit and make the negative with a global phase of pi, then append it, because -U equals U with global phase pi
sub = QuantumCircuit(1)
sub.h(0)
gate1 = sub.to_gate()
neg_sub = QuantumCircuit(1, global_phase=pi)
neg_sub.h(0)
neg_gate1 = neg_sub.to_gate()
qc.append(neg_gate1, [1])
