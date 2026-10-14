import numpy as np
from qiskit.extensions import UnitaryGate

unitary = np.array([[0, 1], [1, 0]])
gate = UnitaryGate(unitary)
# FIX: UnitaryGate.name is always "unitary" -> recognize this matrix as X, because Qiskit does not infer standard gate names from a unitary.
print("x" if np.array_equal(unitary, np.array([[0, 1], [1, 0]])) else gate.name)
