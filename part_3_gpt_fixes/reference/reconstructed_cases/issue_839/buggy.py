from qiskit import Aer
from qiskit.algorithms import VQE
from qiskit.algorithms.optimizers import COBYLA
from qiskit.circuit.library import TwoLocal
from qiskit.opflow import PauliSumOp
from qiskit.quantum_info import Pauli
from qiskit.utils import QuantumInstance

# Simple Hamiltonian
hamiltonian = PauliSumOp.from_list([("ZZ", 1.0), ("XX", 0.5)])

ansatz = TwoLocal(rotation_blocks="ry", entanglement_blocks="cz", num_qubits=2, reps=1)
optimizer = COBYLA(maxiter=50)

backend = Aer.get_backend("statevector_simulator")
qi = QuantumInstance(backend)

vqe = VQE(ansatz=ansatz, optimizer=optimizer, quantum_instance=qi)
result = vqe.compute_minimum_eigenvalue(hamiltonian)

# User expected optimizer_evals to hold the number of function evaluations,
# but it is never set and remains None.
print("optimizer_evals:", result.optimizer_evals)
