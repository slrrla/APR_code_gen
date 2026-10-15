import numpy as np
from qiskit import QuantumCircuit
from qiskit.opflow import I, X, Y, Z

circuit = QuantumCircuit(1, name='R')
# FIX: appended a non-gate opflow operator directly to the circuit, so to_gate() fails -> add its unitary matrix via circuit.unitary, because unitary() creates a proper gate instruction
circuit.unitary((0.5*I - 1j*np.sqrt(1-0.5**2)*Y).to_matrix(), [0])
circuit.to_gate()
