import numpy as np
from qiskit import QuantumCircuit
from qiskit.opflow import I, X, Y, Z

circuit = QuantumCircuit(1, name='R')
# FIX: appended a non-gate opflow operator (becomes a generic instruction that to_gate() rejects) -> convert it to a matrix and add it with circuit.unitary, which creates a UnitaryGate, because a unitary gate can be converted by to_gate()
circuit.unitary((0.5*I - 1j*np.sqrt(1-0.5**2)*Y).to_matrix(), [0])
circuit.to_gate()
