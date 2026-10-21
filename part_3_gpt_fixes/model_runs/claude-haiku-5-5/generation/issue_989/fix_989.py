from qiskit import QuantumCircuit
# FIX: `Aer` imported from `qiskit` (removed in Qiskit 1.0+) -> import it from `qiskit_aer`, because the Aer provider now ships in the separate qiskit-aer package
from qiskit_aer import Aer

print(Aer.backends())
