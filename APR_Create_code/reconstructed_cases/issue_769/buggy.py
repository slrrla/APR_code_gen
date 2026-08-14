import numpy as np
from qiskit.extensions import UnitaryGate

# Attempt to get the gate name directly from a UnitaryGate built from the matrix
unitary = np.array([[0, 1], [1, 0]])
gate = UnitaryGate(unitary)
print(gate.name)  # expected "XGate" but only prints the generic "unitary" label
