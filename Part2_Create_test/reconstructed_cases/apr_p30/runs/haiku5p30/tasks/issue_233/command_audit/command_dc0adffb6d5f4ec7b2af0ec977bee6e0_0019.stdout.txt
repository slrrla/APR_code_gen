from qiskit.circuit.library import n_local
import numpy as np

num_qubits = 2

rot = n_local(
    int(np.sum(num_qubits)),
    "ry",
    [],
    reps=1,
    skip_final_rotation_layer=True,
    parameter_prefix="p",
)
var = n_local(
    int(np.sum(num_qubits)),
    "ry",
    "cx",
    entanglement="linear",
    reps=1,
    skip_final_rotation_layer=True,
)

print(rot.num_parameters)  # >> 2

rot.compose(var, inplace=True)

print(rot.num_parameters)  # >> 4 (updated to reflect combined parameters)
