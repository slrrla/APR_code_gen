from qiskit import QuantumCircuit

state = [0.5, 0.5, 0.5, 0.5]

qc_gate = QuantumCircuit(2)
# FIX: initialize is non-unitary and cannot be converted to a controlled gate -> use prepare_state, because it creates a unitary state-preparation operation
qc_gate.prepare_state(state, [0, 1])

gate = qc_gate.to_gate().control(2)
