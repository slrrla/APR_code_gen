import numpy as np
from qiskit import QuantumCircuit
from qiskit.opflow import I, X, Y, Z

circuit = QuantumCircuit(1, name='R')
circuit.append(0.5*I - 1j*np.sqrt(1-0.5**2)*Y, [0])
circuit.to_gate()
