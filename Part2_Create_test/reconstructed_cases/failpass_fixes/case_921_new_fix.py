from qiskit.quantum_info import SparsePauliOp
import numpy as np

op = SparsePauliOp.from_list([("ZZII", 1.0)])
matrix = op.to_matrix()
eigenvalues = np.linalg.eigvalsh(matrix)
print("Minimum eigenvalue:", eigenvalues[0])
