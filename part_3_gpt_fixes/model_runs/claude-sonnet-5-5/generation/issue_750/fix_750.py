# NO BUG: The code matches the documented tutorial example, and its output is correct (Z on qubit 0 and X on qubit 2).
import numpy as np
from qiskit.quantum_info import Operator, Pauli

op = Operator(np.eye(2 ** 3))
XZ = Operator(Pauli(label='XZ'))
result = op.compose(XZ, qargs=[0, 2])
print(result)
