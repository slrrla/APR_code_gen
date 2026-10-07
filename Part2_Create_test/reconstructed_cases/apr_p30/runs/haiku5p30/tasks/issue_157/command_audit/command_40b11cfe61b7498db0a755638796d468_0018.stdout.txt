from qiskit import QuantumCircuit
from qiskit.circuit.library import StatePreparation

# Attempt to build a controlled initialization gate.
# StatePreparation is a Gate (unlike Initialize which is an Instruction),
# so it can be converted with .to_gate()/.control()
state = [0.5, 0.5, 0.5, 0.5]

qc_gate = QuantumCircuit(2)
qc_gate.append(StatePreparation(state), [0, 1])

# This should work because StatePreparation is a Gate
gate = qc_gate.to_gate().control(2)
