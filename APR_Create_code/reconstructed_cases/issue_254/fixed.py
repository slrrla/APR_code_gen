# Migration from qiskit 0.46.0 to qiskit 1.0 - VQE example
# Fix: qiskit-algorithms is now a separate package; import VQE from qiskit_algorithms

from qiskit.quantum_info import SparsePauliOp
from qiskit.circuit.library import EfficientSU2

from qiskit_algorithms.optimizers import COBYLA
from qiskit_algorithms import VQE
from qiskit.primitives import Estimator

hamiltonian = SparsePauliOp.from_list([("II", 1.0), ("ZZ", -1.0)])

ansatz = EfficientSU2(hamiltonian.num_qubits)

optimizer = COBYLA(maxiter=100)

vqe = VQE(Estimator(), ansatz, optimizer)

result = vqe.compute_minimum_eigenvalue(hamiltonian)
print(result)
