from qiskit import QuantumCircuit
from qiskit.circuit.library import StatePreparation

# Prepare the desired state with a unitary operation, which can be controlled.
state = [0.5, 0.5, 0.5, 0.5]

qc_gate = QuantumCircuit(2)
qc_gate.append(StatePreparation(state), [0, 1])

gate = qc_gate.to_gate().control(2)
