import numpy as np
from qiskit.quantum_info import Operator, Pauli

op = Operator(np.eye(2 ** 3))
XZ = Operator(Pauli(label='XZ'))
result = op.compose(XZ, qargs=[0, 2])
print(result)
