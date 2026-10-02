from qiskit.quantum_info import SparsePauliOp
import numpy as np
hamiltonian = SparsePauliOp.from_list([("ZZII", 1)])
answer = np.linalg.eigvalsh(hamiltonian.to_matrix())[0]
