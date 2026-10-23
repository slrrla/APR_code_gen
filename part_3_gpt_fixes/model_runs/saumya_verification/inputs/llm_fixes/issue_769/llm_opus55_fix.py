import numpy as np
# FIX: qiskit.extensions was removed in Qiskit 1.0 -> import UnitaryGate from qiskit.circuit.library, because that is its current location
from qiskit.circuit.library import UnitaryGate

unitary = np.array([[0, 1], [1, 0]])
gate = UnitaryGate(unitary)
print(gate.name)
