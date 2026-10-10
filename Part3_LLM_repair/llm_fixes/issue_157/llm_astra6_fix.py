from qiskit import QuantumCircuit

state = [0.5, 0.5, 0.5, 0.5]

qc_gate = QuantumCircuit(2)
# FIX: initialize includes nonunitary resets -> use prepare_state, because unitary state preparation can be converted to a controlled gate.
qc_gate.prepare_state(state, [0, 1])

gate = qc_gate.to_gate().control(2)

