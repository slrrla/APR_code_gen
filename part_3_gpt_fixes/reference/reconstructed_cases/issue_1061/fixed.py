import numpy as np
from qiskit.algorithms import VQE
from qiskit.algorithms.optimizers import COBYLA
from qiskit.utils import algorithm_globals
from qiskit.circuit.library import EfficientSU2
from qiskit.quantum_info import SparsePauliOp
from qiskit_aer.primitives import Estimator as AerEstimator
from qiskit_aer import AerError

seed = 170
algorithm_globals.random_seed = seed

# Simple placeholder Hamiltonian (H2-like, 2 qubits) standing in for the LiH problem
hamiltonian = SparsePauliOp.from_list([
    ("II", -1.052373245772859),
    ("IZ", 0.39793742484318045),
    ("ZI", -0.39793742484318045),
    ("ZZ", -0.01128010425623538),
    ("XX", 0.18093119978423156),
])
ref_value = -1.857275030202379

ansatz = EfficientSU2(hamiltonian.num_qubits)
optimizer = COBYLA(maxiter=1000)

# Fix: set approximation=True and shots=None (via run_options) so the AerEstimator
# computes exact expectation values instead of sampling with shot noise.
try:
    noiseless_estimator = AerEstimator(
        run_options={"seed": seed, "shots": None},
        transpile_options={"seed_transpiler": seed},
        approximation=True,
    )
    noiseless_estimator.set_options(device='GPU')
except AerError as e:
    print("Failed to initialize GPU estimator:", str(e))
    noiseless_estimator = AerEstimator(
        run_options={"seed": seed, "shots": None},
        transpile_options={"seed_transpiler": seed},
        approximation=True,
    )

vqe = VQE(noiseless_estimator, ansatz=ansatz, optimizer=optimizer)
vqe.initial_point = np.zeros(ansatz.num_parameters)
result = vqe.compute_minimum_eigenvalue(hamiltonian)

print(result)
print(f"VQE on Aer Estimator (no noise): {result.optimal_value.real:.8f}")
print(f"Delta from reference energy value is {(result.optimal_value.real - ref_value):.8f}")
