from qiskit import QuantumCircuit

# State preparation is a unitary gate (unlike initialize, which resets
# its qubits), so it can be made conditional on control qubits.
# It prepares the same state as initialize when the target starts in |00>.
state = [0.5, 0.5, 0.5, 0.5]

qc_gate = QuantumCircuit(2)
qc_gate.prepare_state(state, [0, 1])
gate = qc_gate.to_gate().control(2)
