from qiskit import QuantumCircuit
# FIX: `from qiskit import Aer` was removed in Qiskit 1.0 -> import Aer from qiskit_aer, because Aer now lives in the separate qiskit_aer package (which provides aer_simulator)
from qiskit_aer import Aer

print(Aer.backends())
