from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
import math

qc = QuantumCircuit(1)
qc.ry(2 * math.pi / 4, 0)

# Verify the hand-calculated probabilities using the statevector simulator
state = Statevector.from_instruction(qc)
probabilities = state.probabilities()

theta = 2 * math.pi / 4
p0 = math.cos(theta / 2) ** 2
p1 = math.sin(theta / 2) ** 2

print("Computed P(0) =", probabilities[0], "Expected P(0) =", p0)
print("Computed P(1) =", probabilities[1], "Expected P(1) =", p1)
