import numpy as np
from qiskit import BasicAer, QuantumCircuit
from qiskit.algorithms import QAOA
from qiskit.algorithms.optimizers import COBYLA
# FIX: The circuit is not an OperatorBase -> import CircuitOp, because it provides conversion to a Pauli operator.
from qiskit.opflow import CircuitOp

nqubits = 4
H = QuantumCircuit(nqubits)
for i in range(nqubits):
    H.z(i)

qaoa = QAOA(optimizer=COBYLA(), reps=1, mixer=H,
            initial_point=np.array([1.0]),
            quantum_instance=BasicAer.get_backend('statevector_simulator'))

# FIX: compute_minimum_eigenvalue received a QuantumCircuit -> convert H to a Pauli operator, because it requires an observable rather than a circuit.
print(qaoa.compute_minimum_eigenvalue(CircuitOp(H).to_pauli_op()))
