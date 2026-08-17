import numpy as np
from qiskit import Aer
from qiskit.aqua.algorithms import VQE
from qiskit.aqua.components.optimizers import COBYLA
from qiskit.aqua.components.variational_forms import RYRZ
from qiskit.aqua.operators import MatrixOperator

np.random.seed = 75
matrix = np.random.rand(16, 16)

qubitOp = MatrixOperator(matrix)
print(qubitOp)
backend = Aer.get_backend('statevector_simulator')
var_form = RYRZ(qubitOp.num_qubits, 10)
optim = COBYLA()
vqe = VQE(qubitOp, var_form, optim)

result_vqe = vqe.run(backend)
print(qubitOp)  # prints operator properties
print('energy', result_vqe['energy'], '\n')
print(result_vqe)
