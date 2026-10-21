from qiskit import QuantumCircuit
from qiskit.circuit.library import StatePreparation

state = [0.5, 0.5, 0.5, 0.5]

qc_gate = QuantumCircuit(2)
# FIX: initialize includes a non-unitary reset so it cannot become a controlled gate -> use StatePreparation, because it is a unitary gate that supports to_gate().control()
qc_gate.append(StatePreparation(state), [0, 1])

gate = qc_gate.to_gate().control(2)
