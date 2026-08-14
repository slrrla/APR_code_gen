from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from math import sqrt

# One qubit circuit, just for reference
qc = QuantumCircuit(1)

# A valid two-level (qubit) statevector
sv1 = Statevector([sqrt(0.3), sqrt(0.7)])
print(sv1)

# Author mistakenly assumes this still describes a single qubit
# with three "basis states" |0>, |1>, |2>
sv2 = Statevector([sqrt(0.2), sqrt(0.2), sqrt(0.6)])
print(sv2)
print(sv2.dims())
