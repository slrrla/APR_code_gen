from qiskit.opflow.primitive_ops import PrimitiveOp
from qiskit.quantum_info import Pauli
import numpy as np

x = 3.5 * np.sqrt(3.0 / 2)
print(x)

annih_op = PrimitiveOp(Pauli('X')) + 1.0j * PrimitiveOp(Pauli('Y'))
creat_op = PrimitiveOp(Pauli('X')) - 1.0j * PrimitiveOp(Pauli('Y'))

# FIX: NumPy scalar multiplication dispatches to an ndarray -> multiply the operator by the scalar, because this keeps the result a Qiskit operator
my_op = creat_op.compose(annih_op, front=True) * x

print('type(my_op) = ', type(my_op))
print('my_op)= ', my_op)

