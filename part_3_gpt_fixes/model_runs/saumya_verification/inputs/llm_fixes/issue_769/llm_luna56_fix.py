import numpy as np
# FIX: import UnitaryGate from its current module and add XGate for recognition, because UnitaryGate alone does not identify standard gates
from qiskit.circuit.library import UnitaryGate, XGate

unitary = np.array([[0, 1], [1, 0]])
# FIX: select the matching standard gate instead of leaving the matrix as a generic unitary, because UnitaryGate.name is always "unitary"
gate = XGate() if np.allclose(unitary, XGate().to_matrix()) else UnitaryGate(unitary)
print(gate.name)
