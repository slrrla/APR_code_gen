import numpy as np
from qiskit import BasicAer, QuantumCircuit
from qiskit.algorithms import QAOA
from qiskit.algorithms.optimizers import COBYLA
# FIX: missing opflow/quantum_info imports -> import PauliSumOp, Operator, SparsePauliOp, because they are needed to convert the circuit into an OperatorBase
from qiskit.opflow import PauliSumOp
from qiskit.quantum_info import Operator, SparsePauliOp

nqubits = 4
H = QuantumCircuit(nqubits)
for i in range(nqubits):
    H.z(i)

qaoa = QAOA(optimizer=COBYLA(), reps=1, mixer=H,
            initial_point=np.array([1.0]),
            quantum_instance=BasicAer.get_backend('statevector_simulator'))

# FIX: passed a QuantumCircuit as the observable -> convert it to a PauliSumOp, because compute_minimum_eigenvalue requires an OperatorBase (Pauli-based for QAOA evolution)
print(qaoa.compute_minimum_eigenvalue(PauliSumOp(SparsePauliOp.from_operator(Operator(H)))))
