# NO BUG: The code is the tutorial's subsystem composition example, and its output is correct: Pauli labels are little-endian, so 'XZ' applies Z to qubit 0 and X to qubit 2, which matches the printed matrix (e.g., column 0 maps to row 4 with +1, column 1 maps to row 5 with -1).
import numpy as np
from qiskit.quantum_info import Operator, Pauli

op = Operator(np.eye(2 ** 3))
XZ = Operator(Pauli(label='XZ'))
result = op.compose(XZ, qargs=[0, 2])
print(result)
