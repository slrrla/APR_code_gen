from qiskit import QuantumCircuit

# Attempt to build a controlled initialization gate.
# QuantumCircuit.initialize() is not a Gate, so calling .to_gate()
# on a circuit that contains an Initialize instruction fails.
state = [0.5, 0.5, 0.5, 0.5]

qc_gate = QuantumCircuit(2)
qc_gate.initialize(state, [0, 1])

# This raises an error because Initialize is not a Gate and
# cannot be converted with .to_gate()/.control()
gate = qc_gate.to_gate().control(2)
