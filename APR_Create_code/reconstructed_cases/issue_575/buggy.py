import numpy as np
from qiskit.circuit.library import ZFeatureMap
from qiskit.quantum_info import Statevector

x = 1

#### Manual Implementation
H = (1 / np.sqrt(2)) * np.array([[1, 1], [1, -1]])
rz_2x = np.array([
    [np.exp(-1j * 2 * x), 0],
    [0, np.exp(1j * 2 * x)]
])
initialState = np.array([1, 0])
manual_state = rz_2x @ (H @ initialState)

#### Qiskit
zfm = ZFeatureMap(1, reps=1)
zfm = zfm.assign_parameters([x])
qiskit_state = Statevector.from_instruction(zfm)

print("Manual:", manual_state)
print("Qiskit:", qiskit_state.data)
