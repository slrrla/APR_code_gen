from qiskit.circuit.library import TwoLocal
from qiskit.opflow import X, Y, Z, I
from qiskit.utils import QuantumInstance
from qiskit import *
from qiskit.algorithms.optimizers import COBYLA
from qiskit.algorithms import VQE

# Manual, non-scalable construction of a Hamiltonian using individual Pauli operators
weights = [i for i in range(1, 4)]
hamiltonian = weights[0]*(Z^Z^I) + weights[1]*(Z^I^Z) + weights[2]*(I^Z^Z)

num_qubits = hamiltonian.num_qubits
ansatz = TwoLocal(num_qubits, ['ry', 'rz'], 'cx', 'linear', reps=1, insert_barriers=True)
qi = QuantumInstance(Aer.get_backend('statevector_simulator'))
optimizer = COBYLA(maxiter=100)
vqe = VQE(ansatz, optimizer=optimizer, quantum_instance=qi)
result = vqe.compute_minimum_eigenvalue(hamiltonian)

print(hamiltonian)
