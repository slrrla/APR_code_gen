from qiskit import transpile
from qiskit import Aer
import numpy as np
from qiskit.opflow import MatrixOp
from qiskit.circuit.library import EfficientSU2
from qiskit.algorithms.optimizers import COBYLA
from qiskit.providers.aer import AerSimulator
from qiskit.utils import QuantumInstance
from qiskit.providers.fake_provider import FakeSherbrooke
from qiskit.algorithms import VQE

# backend = Aer.get_backend('qasm_simulator')
# backend = AerSimulator()
backend = FakeSherbrooke()

Hamiltonian = [
    [4.07981221, -3.6713615, 1.3943662, -1.05164319],
    [-3.6713615, 5.88262911, -4.14084507, 1.37558685],
    [1.3943662, -4.14084507, 5.83098592, -3.54929577],
    [-1.05164319, 1.37558685, -3.54929577, 3.79812207]
]
H_op = MatrixOp(Hamiltonian).to_pauli_op()

ansatz = EfficientSU2(num_qubits=2, entanglement='linear', reps=5, skip_final_rotation_layer=True)
ansatz_opt = transpile(circuits=ansatz, backend=backend, optimization_level=3)

# FIX: apply the ansatz's layout to the Hamiltonian so its qubit count
# matches the transpiled ansatz on the 127-qubit backend.
H_op = H_op.apply_layout(ansatz_opt.layout)

optimizer = COBYLA(maxiter=1500)

quantum_instance = QuantumInstance(
    backend=backend,
    shots=1024,
    seed_simulator=28,
    basis_gates=None,
    optimization_level=2
)

initial_point_values = 2 * np.pi * np.random.rand(ansatz_opt.num_parameters)

vqe = VQE(
    ansatz=ansatz_opt,
    optimizer=optimizer,
    quantum_instance=quantum_instance,
    initial_point=initial_point_values
)
result = vqe.compute_minimum_eigenvalue(H_op)
print(result)
