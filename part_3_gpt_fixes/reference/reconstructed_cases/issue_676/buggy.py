from qiskit import Aer
from qiskit.circuit.library import EfficientSU2
from qiskit.opflow import PauliSumOp
from qiskit.algorithms import VQE
from qiskit.algorithms.optimizers import SPSA
from qiskit.quantum_info import SparsePauliOp

N_iters = 5

# Example Hamiltonian
H = SparsePauliOp.from_list([("ZZIII", 1.0), ("IZZII", 1.0), ("IIZZI", 1.0), ("IIIZZ", 1.0), ("ZIIIZ", 1.0)])
H_op = PauliSumOp(H)

circ_ansatz = EfficientSU2(5, reps=1)

# BUG: passing the optimizer class itself instead of an instance
my_vqe = VQE(ansatz=circ_ansatz, optimizer=SPSA, quantum_instance=Aer.get_backend('aer_simulator'), initial_point=[0.5]*N_iters)

print(my_vqe.compute_minimum_eigenvalue(H_op))
