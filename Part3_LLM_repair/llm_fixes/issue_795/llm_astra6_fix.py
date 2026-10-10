import numpy as np
from qiskit import QuantumCircuit
from qiskit.opflow import I, X, Y, Z

circuit = QuantumCircuit(1, name='R')
# FIX: Appending the opflow expression creates a non-gate instruction -> add its matrix as a unitary gate, because to_gate() requires gate instructions.
circuit.unitary((0.5*I - 1j*np.sqrt(1-0.5**2)*Y).to_matrix(), [0])
circuit.to_gate()

