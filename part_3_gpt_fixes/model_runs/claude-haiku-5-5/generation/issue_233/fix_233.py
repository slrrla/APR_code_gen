from qiskit.circuit.library import TwoLocal
import numpy as np

num_qubits = 2

rot = TwoLocal(
    int(np.sum(num_qubits)),
    "ry",
    [],
    reps=1,
    skip_final_rotation_layer=True,
    parameter_prefix="p",
)
var = TwoLocal(
    int(np.sum(num_qubits)),
    "ry",
    "cx",
    entanglement="linear",
    reps=1,
    skip_final_rotation_layer=True,
)

print(rot.num_parameters_settable())

# FIX: blueprint circuit rot was lazily built, so the inplace compose was discarded when parameters were later accessed -> build rot before composing, because a built circuit keeps the appended gates
rot._build()
rot.compose(var, inplace=True)

print(rot.num_parameters_settable())
