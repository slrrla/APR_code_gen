from qiskit import QuantumCircuit
import numpy as np

n = 2
circuit = QuantumCircuit(n, n)

# Seeking some sort of initialization routine like this
circuit.initializeQubits(initialState=np.ones(n))

# Define rest of the circuit
circuit.measure(range(n), range(n))
