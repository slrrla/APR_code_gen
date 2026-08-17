from qiskit import QuantumCircuit
from qiskit.extensions import UnitaryGate
import numpy as np

# Author wants to know how Qiskit decomposes an arbitrary unitary
# when it's added to a circuit via UnitaryGate.
unitary_matrix = np.array([[1, 0], [0, 1]])  # placeholder 2x2 unitary

qc = QuantumCircuit(1)
gate = UnitaryGate(unitary_matrix)
qc.append(gate, [0])

print(qc.decompose())
