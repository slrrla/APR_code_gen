from qiskit import QuantumCircuit
# FIX: `from qiskit import Aer` no longer exists -> import Aer from qiskit_aer, because Aer was moved out of the qiskit package into the separate qiskit_aer package
from qiskit_aer import Aer

print(Aer.backends())

