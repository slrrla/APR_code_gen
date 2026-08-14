from qiskit import Aer
from qiskit.aqua.algorithms import QAOA
from qiskit.aqua.components.optimizers import COBYLA
from qiskit.aqua.operators import Zero, I, Z

# simple Hamiltonian for a toy problem
H = (Z ^ Z) - (I ^ I)

p = 1
optimizer = COBYLA()

# BUG: initial_state is passed as the bare Zero class/instance without
# specifying the number of qubits, which QAOA cannot use as-is.
qaoa_mes = QAOA(H, p=p, optimizer=optimizer, initial_state=Zero,
                quantum_instance=Aer.get_backend("qasm_simulator"))
results = qaoa_mes.run()
