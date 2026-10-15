from qiskit import QuantumCircuit
# FIX: import StatePreparation, a unitary state-prep gate, because initialize contains a reset and cannot be made a controlled gate
from qiskit.circuit.library import StatePreparation

state = [0.5, 0.5, 0.5, 0.5]

qc_gate = QuantumCircuit(2)
# FIX: initialize (non-unitary, includes reset) -> append StatePreparation(state), because it is a unitary gate that to_gate() and control() can handle
qc_gate.append(StatePreparation(state), [0, 1])

gate = qc_gate.to_gate().control(2)
