import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

n = 20
new_state = np.zeros(2 ** n)
new_state[0] = 1.0
print(new_state.shape)

qc3 = QuantumCircuit(n)
qc3.initialize(new_state)

statevector = Statevector(qc3)
print(statevector.dim)
