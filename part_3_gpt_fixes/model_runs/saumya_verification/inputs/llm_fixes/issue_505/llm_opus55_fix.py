from qiskit.opflow.primitive_ops import PrimitiveOp
from qiskit.quantum_info import Pauli
import numpy as np

# FIX: x was a numpy.float64 whose __mul__ broadcasts over the operator into a nested ndarray -> cast to Python float, because float defers to the operator's __rmul__ for proper scalar multiplication
x = float(3.5 * np.sqrt(3.0 / 2))
print(x)

annih_op = PrimitiveOp(Pauli('X')) + 1.0j * PrimitiveOp(Pauli('Y'))
creat_op = PrimitiveOp(Pauli('X')) - 1.0j * PrimitiveOp(Pauli('Y'))

my_op = x * creat_op.compose(annih_op, front=True)

print('type(my_op) = ', type(my_op))
print('my_op)= ', my_op)
