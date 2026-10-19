import numpy as np
from qiskit import QuantumCircuit
from qiskit.extensions import UnitaryGate

# Attempt to directly turn the Hamiltonian matrix A into a gate,
# as if it were a rotation analogous to Pauli-X rotation.
A = 1 / (2 * np.sqrt(2)) * np.array([
    [0, 1, 1, 0],
    [1, 0, 0, 1],
    [1, 0, 0, 1],
    [0, 1, 1, 0]
])

# This fails: A is Hermitian but NOT unitary, so UnitaryGate rejects it.
gate = UnitaryGate(A)

circ = QuantumCircuit(2)
circ.append(gate, [0, 1])
circ.draw('mpl')
