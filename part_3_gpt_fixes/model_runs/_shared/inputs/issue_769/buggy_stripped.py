import numpy as np
from qiskit.extensions import UnitaryGate

unitary = np.array([[0, 1], [1, 0]])
gate = UnitaryGate(unitary)
print(gate.name)
