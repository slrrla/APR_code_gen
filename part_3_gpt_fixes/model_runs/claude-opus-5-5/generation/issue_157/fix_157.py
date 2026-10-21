from qiskit import QuantumCircuit

state = [0.5, 0.5, 0.5, 0.5]

qc_gate = QuantumCircuit(2)
# FIX: initialize contains non-unitary reset operations so to_gate()/control() fails -> use prepare_state, because StatePreparation is a unitary gate that can be converted to a gate and controlled
qc_gate.prepare_state(state, [0, 1])

gate = qc_gate.to_gate().control(2)
