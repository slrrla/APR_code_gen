from qiskit import QuantumCircuit
# FIX: imported Aer from the removed qiskit.Aer location -> import it from qiskit_aer, because Aer was moved into the separate qiskit_aer package (use AerSimulator / Aer.get_backend('aer_simulator') for the ideal simulator)
from qiskit_aer import Aer

print(Aer.backends())
