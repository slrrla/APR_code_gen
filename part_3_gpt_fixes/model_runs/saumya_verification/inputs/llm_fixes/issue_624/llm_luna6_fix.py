import numpy as np
from qiskit import BasicAer, QuantumCircuit
from qiskit.algorithms import QAOA
from qiskit.algorithms.optimizers import COBYLA
# FIX: the circuit is not an observable -> convert its unitary to an opflow operator, because QAOA expects an OperatorBase.
from qiskit.quantum_info import Operator
from qiskit.opflow import PauliSumOp

nqubits = 4
H = QuantumCircuit(nqubits)
for i in range(nqubits):
    H.z(i)

qaoa = QAOA(optimizer=COBYLA(), reps=1, mixer=H,
            initial_point=np.array([1.0]),
            quantum_instance=BasicAer.get_backend('statevector_simulator'))

# FIX: compute_minimum_eigenvalue cannot take a QuantumCircuit -> convert it to PauliSumOp, because the circuit itself is not an observable.
print(qaoa.compute_minimum_eigenvalue(PauliSumOp.from_operator(Operator(H))))
