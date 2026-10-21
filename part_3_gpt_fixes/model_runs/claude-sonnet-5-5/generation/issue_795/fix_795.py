import numpy as np
from qiskit import QuantumCircuit
from qiskit.opflow import I, X, Y, Z

circuit = QuantumCircuit(1, name='R')
# FIX: appended an opflow operator, which is not a Gate -> append its matrix as a unitary gate, because UnitaryGate is a Gate so to_gate() succeeds
circuit.unitary((0.5*I - 1j*np.sqrt(1-0.5**2)*Y).to_matrix(), [0])
circuit.to_gate()
