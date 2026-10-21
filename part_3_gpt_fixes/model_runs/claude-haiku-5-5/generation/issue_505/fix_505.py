from qiskit.opflow.primitive_ops import PrimitiveOp
from qiskit.quantum_info import Pauli
import numpy as np

# FIX: x was a numpy.float64, so numpy treated the PrimitiveOp as an array-like and broadcast into a nested object array -> wrapped the value in float() to get a Python float, because a Python float scalar dispatches to PrimitiveOp.__rmul__ and keeps the result as a PauliSumOp.
x = float(3.5 * np.sqrt(3.0 / 2))
print(x)

annih_op = PrimitiveOp(Pauli('X')) + 1.0j * PrimitiveOp(Pauli('Y'))
creat_op = PrimitiveOp(Pauli('X')) - 1.0j * PrimitiveOp(Pauli('Y'))

my_op = x * creat_op.compose(annih_op, front=True)

print('type(my_op) = ', type(my_op))
print('my_op)= ', my_op)
