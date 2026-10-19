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

# optimizer_evals is no longer populated since the refactor in PR #6418;
# the actual number of evaluations is stored in cost_function_evals.
print("cost_function_evals:", result.cost_function_evals)
