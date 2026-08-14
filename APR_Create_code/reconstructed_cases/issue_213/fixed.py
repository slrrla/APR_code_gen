from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from math import sqrt

# One qubit circuit, just for reference
qc = QuantumCircuit(1)

# A valid two-level (qubit) statevector
sv1 = Statevector([sqrt(0.3), sqrt(0.7)])
print(sv1)

# Statevector can represent systems of arbitrary subsystem dimensions.
# A 6-dimensional vector can be explicitly split into a 2-level and
# a 3-level subsystem using the dims argument.
psi = Statevector(
    [1 / sqrt(6), 1 / sqrt(6), 1 / sqrt(6), 1 / sqrt(6), 1 / sqrt(6), 1 / sqrt(6)],
    dims=(2, 3),
)
print(psi)
print(psi.dims())
