from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import StatePreparation
import numpy as np

circuit = QuantumCircuit(
    QuantumRegister(1, "a"),
    QuantumRegister(1, "b"),
    QuantumRegister(2, "state")
)

state = [0, 1/np.sqrt(2), -1.j/np.sqrt(2), 0]
controlled_gate = StatePreparation(state).control(2)

circuit.append(controlled_gate, circuit.qubits)
circuit.draw()
