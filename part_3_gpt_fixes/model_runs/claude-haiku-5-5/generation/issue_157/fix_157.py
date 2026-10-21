from qiskit import QuantumCircuit
# FIX: StatePreparation was not imported -> added the import, because the fix needs the StatePreparation gate
from qiskit.circuit.library import StatePreparation

state = [0.5, 0.5, 0.5, 0.5]

qc_gate = QuantumCircuit(2)
# FIX: qc_gate.initialize(state, [0, 1]) adds a reset, which makes the circuit non-unitary so to_gate() fails -> append a StatePreparation gate instead, because it prepares the state without a reset and is a convertible gate
qc_gate.append(StatePreparation(state), [0, 1])

gate = qc_gate.to_gate().control(2)
