from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import StatePreparation
import numpy as np

a = QuantumRegister(2, "a")
b = QuantumRegister(2, "b")
circuit = QuantumCircuit(a, b)

state = [0, 1/np.sqrt(2), -1.j/np.sqrt(2), 0]
circuit.initialize(state)

controlled_gate = StatePreparation(state).control()
