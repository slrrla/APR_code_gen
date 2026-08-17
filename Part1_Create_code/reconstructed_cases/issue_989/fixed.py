from qiskit import QuantumCircuit
from qiskit_aer import Aer

# After upgrading qiskit/qiskit-aer, aer_simulator is available
print(Aer.backends())
