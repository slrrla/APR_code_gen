from qiskit import QuantumCircuit

state = [0.5, 0.5, 0.5, 0.5]

qc_gate = QuantumCircuit(2)
qc_gate.initialize(state, [0, 1])

gate = qc_gate.to_gate().control(2)
