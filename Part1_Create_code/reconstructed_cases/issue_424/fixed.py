import numpy as np
from qiskit.circuit.library import EfficientSU2
from qiskit.quantum_info import SparsePauliOp, Statevector
from qiskit.algorithms import TimeEvolutionProblem
from qiskit.algorithms.time_evolvers.variational import VarQITE, ImaginaryMcLachlanPrinciple
from qiskit.algorithms.gradients import ReverseEstimatorGradient, ReverseQGT

num_qubits = 4

# Some example Hamiltonian on 4 qubits
hamiltonian = SparsePauliOp.from_list([
    ("ZZII", 1.0),
    ("IZZI", 1.0),
    ("IIZZ", 1.0),
    ("XIII", 0.5),
    ("IXII", 0.5),
])

# Increase the circuit depth (reps) so the ansatz has enough expressive
# power to represent the true ground state
ansatz = EfficientSU2(num_qubits, reps=3)
init_param_values = {p: np.pi / 4 for p in ansatz.parameters}

gradient = ReverseEstimatorGradient()
qgt = ReverseQGT()
var_principle = ImaginaryMcLachlanPrinciple(qgt=qgt, gradient=gradient)

time = 1.0
evolution_problem = TimeEvolutionProblem(hamiltonian, time)

var_qite = VarQITE(ansatz, init_param_values, var_principle, num_timesteps=100)
evolution_result = var_qite.evolve(evolution_problem)

evolved_state = Statevector(evolution_result.evolved_state).data
print("Evolved statevector =", evolved_state)

exact_eigenvalue = np.min(np.linalg.eigvalsh(hamiltonian.to_matrix()))
print("Exact lowest eigenvalue found :", exact_eigenvalue)
