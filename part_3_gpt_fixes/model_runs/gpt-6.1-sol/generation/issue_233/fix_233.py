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

# FIX: num_parameters_settable() counts the template's parameters -> use num_parameters, because it counts the circuit's actual unbound parameters
print(rot.num_parameters)

rot.compose(var, inplace=True)

# FIX: num_parameters_settable() ignores the composed circuit's parameters -> use num_parameters, because it includes all actual unbound parameters after composition
print(rot.num_parameters)
