from qiskit import QuantumCircuit

# Build a controlled state-preparation unitary for targets initially in |00>.
# Unlike initialize(), prepare_state() does not contain a nonunitary reset.
state = [0.5, 0.5, 0.5, 0.5]

qc_gate = QuantumCircuit(2)
qc_gate.prepare_state(state, [0, 1])

# The state-preparation unitary can be converted to a gate with two controls.
gate = qc_gate.to_gate().control(2)
