# Migration from qiskit 0.46.0 to qiskit 1.0 - VQE example
# Reported bug: ModuleNotFoundError: No module named 'qiskit_algorithms'

from qiskit.quantum_info import SparsePauliOp
from qiskit.circuit.library import EfficientSU2

# NOTE: mixing old qiskit.algorithms import (removed in qiskit 1.0)
# with new qiskit_algorithms package import
from qiskit_algorithms.optimizers import COBYLA
from qiskit.algorithms import VQE

hamiltonian = SparsePauliOp.from_list([("II", 1.0), ("ZZ", -1.0)])

ansatz = EfficientSU2(hamiltonian.num_qubits)

optimizer = COBYLA(maxiter=100)

vqe = VQE(ansatz=ansatz, optimizer=optimizer)

result = vqe.compute_minimum_eigenvalue(hamiltonian)
print(result)
