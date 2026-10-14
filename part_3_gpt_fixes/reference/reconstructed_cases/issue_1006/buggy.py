from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from math import sqrt, pi

qc = QuantumCircuit(3)
qc.initialize(
    [
        0.0 + 0.0j,
        sqrt(1 / 3) + 0.0j,
        0.0 + 0.0j,
        0.0 + 0.0j,
        0.0 + 0.0j,
        0.0 + 0.0j,
        0.0 + 0.0j,
        sqrt(2 / 3) + 0.0j,
    ]
)
qc.cry(pi / 2, 1, 0)  # (theta, controlled bit, target bit)
print(Statevector(qc))
