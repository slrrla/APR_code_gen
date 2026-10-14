from math import pi
from qiskit import QuantumCircuit
from qiskit.circuit.library import GlobalPhaseGate

qc = QuantumCircuit(2)
qc.h([0, 1])
qc.append(GlobalPhaseGate(pi), [])

# Alternative equivalent approach using the global_phase parameter
qc2 = QuantumCircuit(2, global_phase=pi)
qc2.h([0, 1])
