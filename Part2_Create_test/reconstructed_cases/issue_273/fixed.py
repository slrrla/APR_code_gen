from qiskit import Aer
from qiskit.aqua.algorithms import QAOA
from qiskit.aqua.components.optimizers import COBYLA
from qiskit.aqua.operators import Zero, I, Z

# simple Hamiltonian for a toy problem
H = (Z ^ Z) - (I ^ I)

p = 1
optimizer = COBYLA()

# FIX: give Zero the number of qubits so it can build a valid initial state
n_qubits = 2  # or whatever you want for your example
qaoa_mes = QAOA(H, p=p, optimizer=optimizer, initial_state=Zero(n_qubits),
                quantum_instance=Aer.get_backend("qasm_simulator"))
results = qaoa_mes.run()
