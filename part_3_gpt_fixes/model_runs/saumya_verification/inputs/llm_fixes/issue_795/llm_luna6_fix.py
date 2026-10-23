import numpy as np
from qiskit import QuantumCircuit
from qiskit.opflow import I, X, Y, Z

circuit = QuantumCircuit(1, name='R')
# FIX: the opflow sum is appended as a circuit instruction that to_gate rejects -> append its unitary matrix, because unitary creates a gate instruction
circuit.unitary((0.5*I - 1j*np.sqrt(1-0.5**2)*Y).to_matrix(), [0])
circuit.to_gate()

