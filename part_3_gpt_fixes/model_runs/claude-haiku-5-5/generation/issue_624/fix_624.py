import numpy as np
from qiskit import BasicAer, QuantumCircuit
# FIX: operator class was missing for the cost Hamiltonian -> added SparsePauliOp import, because compute_minimum_eigenvalue needs an operator, not a circuit
from qiskit.quantum_info import SparsePauliOp
from qiskit.algorithms import QAOA
from qiskit.algorithms.optimizers import COBYLA

nqubits = 4
H = QuantumCircuit(nqubits)
for i in range(nqubits):
    H.z(i)

# FIX: passed a QuantumCircuit as the Hamiltonian -> built a SparsePauliOp of the Z terms and pass that to compute_minimum_eigenvalue, because the solver requires an operator
cost_hamiltonian = SparsePauliOp.from_sparse_list([("Z", [i], 1.0) for i in range(nqubits)], num_qubits=nqubits)

# FIX: initial_point had length 1 but reps=1 needs 2 parameters (gamma, beta) -> changed to length 2, because the parameter count must match 2*reps
qaoa = QAOA(optimizer=COBYLA(), reps=1, mixer=H,
            initial_point=np.array([1.0, 1.0]),
            quantum_instance=BasicAer.get_backend('statevector_simulator'))

# FIX: passed the circuit H to compute_minimum_eigenvalue -> pass the cost_hamiltonian operator instead, because the cost must be an operator
print(qaoa.compute_minimum_eigenvalue(cost_hamiltonian))
