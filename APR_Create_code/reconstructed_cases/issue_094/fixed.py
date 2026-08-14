from qiskit.circuit.library import TwoLocal
from qiskit.opflow.primitive_ops import PauliSumOp
from qiskit.utils import QuantumInstance
from qiskit import *
from qiskit.algorithms.optimizers import COBYLA
from qiskit.algorithms import VQE

# Scalable construction of a Hamiltonian using PauliSumOp.from_list
paulis = ['IZ', 'XZ', 'YZ', 'ZZ', 'XX']
weights = [1, 2, 3, 4, 5]
pauli_op = [([pauli, weight]) for pauli, weight in zip(paulis, weights)]
hamiltonian = PauliSumOp.from_list([op for op in pauli_op])

num_qubits = hamiltonian.num_qubits
ansatz = TwoLocal(num_qubits, ['ry', 'rz'], 'cx', 'linear', reps=1, insert_barriers=True)
qi = QuantumInstance(Aer.get_backend('statevector_simulator'))
optimizer = COBYLA(maxiter=100)
vqe = VQE(ansatz, optimizer=optimizer, quantum_instance=qi)
result = vqe.compute_minimum_eigenvalue(hamiltonian)

print(hamiltonian)
