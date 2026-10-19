# NO BUG: The code correctly composes the two-qubit XZ operator onto qubits 0 and 2 and stores the returned operator.
import numpy as np
from qiskit.quantum_info import Operator, Pauli

op = Operator(np.eye(2 ** 3))
XZ = Operator(Pauli(label='XZ'))
result = op.compose(XZ, qargs=[0, 2])
print(result)
