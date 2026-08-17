import math
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

qc = QuantumCircuit(1)
qc.ry(3 * math.pi / 4, 0)

# Compute probability of measuring |0>
state = Statevector.from_instruction(qc)
probabilities = state.probabilities_dict()
prob_zero = probabilities.get('0', 0.0)
print(prob_zero)  # should be approximately 0.1464
