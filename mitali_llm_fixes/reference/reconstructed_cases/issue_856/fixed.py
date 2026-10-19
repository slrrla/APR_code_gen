from qiskit import QuantumCircuit
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.opflow import X, Y
from qiskit.synthesis import QDrift

op = (X ^ X) + (Y ^ Y)
time = 1
reps = 1
evo_gate = PauliEvolutionGate(op, time, synthesis=QDrift(reps=reps))
circ = QuantumCircuit(2)
circ.append(evo_gate, [0, 1])
