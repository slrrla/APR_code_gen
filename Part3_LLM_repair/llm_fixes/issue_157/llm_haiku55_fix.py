from qiskit import QuantumCircuit
# FIX: added import of StatePreparation -> needed to replace initialize, because initialize inserts a reset and cannot be converted to a controllable gate
from qiskit.circuit.library import StatePreparation

state = [0.5, 0.5, 0.5, 0.5]

qc_gate = QuantumCircuit(2)
# FIX: qc_gate.initialize(state, [0, 1]) -> qc_gate.append(StatePreparation(state), [0, 1]), because initialize includes a reset which makes the circuit non-unitary and it cannot be controlled, while StatePreparation is a unitary gate that prepares the same state
qc_gate.append(StatePreparation(state), [0, 1])

gate = qc_gate.to_gate().control(2)
