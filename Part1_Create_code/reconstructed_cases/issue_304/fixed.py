from qiskit.opflow import X, Y, Z
from qiskit.opflow.primitive_ops import MatrixOp
from qiskit.opflow import PauliSumOp
import numpy as np

op = 2*(X^X) + 0.5*(Z^Y)

inv_matrix = np.linalg.inv(op.to_matrix())
operator = MatrixOp(inv_matrix)
print(operator.to_pauli_op())

pauli_list = [(p.primitive.to_label(), p.coeff) for p in operator.to_pauli_op().oplist]
pauli_sum_op = PauliSumOp.from_list(pauli_list)
print(pauli_sum_op)
