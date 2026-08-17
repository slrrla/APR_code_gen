import numpy as np
from qiskit import QuantumCircuit
from qiskit.opflow import I, X, Y, Z

# construct one qubit circuit
circuit = QuantumCircuit(1, name='R')
# build the unitary matrix from the Pauli string and apply it directly
U = (0.5*I - 1j*np.sqrt(1-0.5**2)*Y).to_matrix()
circuit.unitary(U, [0])
gate = circuit.to_gate()
