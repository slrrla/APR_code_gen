from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator
import numpy as np
from qiskit.quantum_info import SparsePauliOp
from qiskit.circuit.library import EfficientSU2
from qiskit_algorithms import VQE
from qiskit_algorithms.optimizers import COBYLA
from qiskit_aer.primitives import Estimator as Estimator

backend = AerSimulator()

Hamiltonian = [
    [ 4.07981221, -3.6713615 ,  1.3943662 , -1.05164319],
    [-3.6713615 ,  5.88262911, -4.14084507,  1.37558685],
    [ 1.3943662 , -4.14084507,  5.83098592, -3.54929577],
    [-1.05164319,  1.37558685, -3.54929577,  3.79812207]
]

H_op = SparsePauliOp.from_operator(Hamiltonian)

ansatz = EfficientSU2(num_qubits=2, entanglement='linear', reps=5, skip_final_rotation_layer=True)

pm = generate_preset_pass_manager(
    optimization_level=3,
    backend=backend,
    basis_gates=None,
    seed_transpiler=28
)
ansatz_opt = pm.run(ansatz)

optimizer = COBYLA(maxiter=1500)

estimator = Estimator(
    run_options={"shots": 1024, "seed": 28},
)

initial_point_values = 2 * np.pi * np.random.rand(ansatz_opt.num_parameters)

vqe = VQE(
    estimator=estimator,
    ansatz=ansatz_opt,
    optimizer=optimizer,
    initial_point=initial_point_values
)

result = vqe.compute_minimum_eigenvalue(H_op)
print(result)
