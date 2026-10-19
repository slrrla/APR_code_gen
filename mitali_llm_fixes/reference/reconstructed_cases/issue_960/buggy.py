import numpy as np
from qiskit import Aer
from qiskit.aqua.algorithms import VQE
from qiskit.aqua.components.optimizers import COBYLA
from qiskit.aqua.components.variational_forms import RYRZ
from qiskit.aqua.operators import MatrixOperator

# original matrix had a non-power-of-2 dimension (e.g. 30x30 slice)
np.random.seed = 75
matrix = np.random.rand(30, 30)

C = matrix
C = C[:, :len(C[0])]
B = matrix
B = B[:, :len(B[0])]
print("Input:", C)

qubitOp = MatrixOperator(C)
print(qubitOp)
backend = Aer.get_backend('statevector_simulator')
var_form = RYRZ(qubitOp.num_qubits, 10)
optim = COBYLA()
vqe = VQE(qubitOp, var_form, optim)

# Runs the VQE over the backend defined above.
result_vqe = vqe.run(backend)
print(qubitOp)  # prints operator properties
print('energy', result_vqe['energy'], '\n')
print(result_vqe)
