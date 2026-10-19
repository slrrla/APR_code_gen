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
# The resulting negative amplitude on |110> is mathematically correct:
# Ry(pi/2) applied to the |1> component (controlled on qubit 1 = 1)
# maps |1> -> (-1/sqrt(2))|0> + (1/sqrt(2))|1>, so the |110> term
# picks up a genuine minus sign; this is not a bug.
print(Statevector(qc))
