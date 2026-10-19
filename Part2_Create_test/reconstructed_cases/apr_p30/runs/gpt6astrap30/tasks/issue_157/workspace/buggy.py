from qiskit import QuantumCircuit

# Use unitary state preparation: initialize also resets the qubits,
# which is non-unitary and cannot be made into a controlled gate.
# The target qubits must start in |00> for this to prepare the state.
state = [0.5, 0.5, 0.5, 0.5]

qc_gate = QuantumCircuit(2)
qc_gate.prepare_state(state, [0, 1])

# Prepare the target state only when both control qubits are |1>.
gate = qc_gate.to_gate().control(2)
