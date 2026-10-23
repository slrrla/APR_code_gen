from qiskit import QuantumCircuit
# FIX: Aer is no longer imported from qiskit -> import it from qiskit_aer, because Aer simulators are provided by the separate Qiskit Aer package.
from qiskit_aer import Aer

print(Aer.backends())

