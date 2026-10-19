import numpy as np
from qiskit import BasicAer, QuantumCircuit
from qiskit.algorithms import QAOA
from qiskit.algorithms.optimizers import COBYLA
# FIX: the circuit is not an OperatorBase observable -> import conversion APIs, because QAOA requires an operator representation
from qiskit.opflow import PauliSumOp
from qiskit.quantum_info import Operator

nqubits = 4
H = QuantumCircuit(nqubits)
for i in range(nqubits):
    H.z(i)

qaoa = QAOA(optimizer=COBYLA(), reps=1, mixer=H,
            initial_point=np.array([1.0]),
            quantum_instance=BasicAer.get_backend('statevector_simulator'))

# FIX: passing a QuantumCircuit is invalid -> convert its unitary to a PauliSumOp, because compute_minimum_eigenvalue expects an OperatorBase
print(qaoa.compute_minimum_eigenvalue(PauliSumOp.from_operator(Operator(H))))
