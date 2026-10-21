import numpy as np
from qiskit import BasicAer, QuantumCircuit
from qiskit.algorithms import QAOA
from qiskit.algorithms.optimizers import COBYLA
from qiskit.opflow import Z

nqubits = 4
# FIX: H was a QuantumCircuit, not an operator -> build H as a Z^4 Pauli operator, because compute_minimum_eigenvalue requires an OperatorBase
H = Z ^ Z ^ Z ^ Z

# FIX: mixer was set to the circuit H and initial_point had 1 entry -> removed the mixer so the default is used and gave 2 initial parameters, because reps=1 needs beta and gamma and the mixer must be a valid mixer
qaoa = QAOA(optimizer=COBYLA(), reps=1,
            initial_point=np.array([1.0, 1.0]),
            quantum_instance=BasicAer.get_backend('statevector_simulator'))

print(qaoa.compute_minimum_eigenvalue(H))
