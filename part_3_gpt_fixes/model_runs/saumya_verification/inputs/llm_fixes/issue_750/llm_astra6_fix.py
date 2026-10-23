import numpy as np
from qiskit.quantum_info import Operator, Pauli

op = Operator(np.eye(2 ** 3))
# FIX: Pauli no longer accepts the label keyword -> pass 'XZ' positionally, because the constructor accepts the Pauli label as its data argument.
XZ = Operator(Pauli('XZ'))
result = op.compose(XZ, qargs=[0, 2])
print(result)

