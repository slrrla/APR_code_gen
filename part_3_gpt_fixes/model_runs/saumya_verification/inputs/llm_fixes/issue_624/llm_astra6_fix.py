import numpy as np
from qiskit import BasicAer, QuantumCircuit
from qiskit.algorithms import QAOA
from qiskit.algorithms.optimizers import COBYLA
# FIX: No circuit-to-operator converter was imported -> import CircuitOp, because it supports conversion to a Pauli observable.
from qiskit.opflow import CircuitOp

nqubits = 4
H = QuantumCircuit(nqubits)
for i in range(nqubits):
    H.z(i)

qaoa = QAOA(optimizer=COBYLA(), reps=1, mixer=H,
            initial_point=np.array([1.0]),
            quantum_instance=BasicAer.get_backend('statevector_simulator'))

# FIX: A QuantumCircuit was passed as the observable -> convert H to a Pauli operator, because compute_minimum_eigenvalue requires an OperatorBase.
print(qaoa.compute_minimum_eigenvalue(CircuitOp(H).to_pauli_op()))

