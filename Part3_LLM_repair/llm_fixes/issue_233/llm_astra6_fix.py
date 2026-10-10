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

# FIX: num_parameters_settable reports template parameters -> use num_parameters, because it counts all free parameters in the circuit.
print(rot.num_parameters)

rot.compose(var, inplace=True)

# FIX: num_parameters_settable does not include composed parameters -> use num_parameters, because it counts all free parameters in the composed circuit.
print(rot.num_parameters)

