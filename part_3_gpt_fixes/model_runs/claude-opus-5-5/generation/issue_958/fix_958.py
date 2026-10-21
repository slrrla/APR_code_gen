from qiskit import QuantumCircuit
# FIX: needed pi to express the -1 factor as a global phase e^{i*pi} = -1
from math import pi

qc = QuantumCircuit(2)
qc.h([0, 1])

gate1 = qc.h
# FIX: `-1 * gate1` multiplied a bound method (TypeError) and applied nothing -> build a 1-qubit circuit with global_phase=pi containing the gate, convert it to a gate and append it, because -U equals U with a global phase of pi and as a gate the phase is kept when it is part of a larger/controlled operation
neg_gate1 = QuantumCircuit(1, global_phase=pi)
neg_gate1.h(0)
qc.append(neg_gate1.to_gate(), [1])
