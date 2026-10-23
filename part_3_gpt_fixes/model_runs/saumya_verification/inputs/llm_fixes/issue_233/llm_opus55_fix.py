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

# FIX: called num_parameters_settable() as a method -> use num_parameters property, because num_parameters_settable is a property (not callable) and only counts the NLocal's own blueprint parameters
print(rot.num_parameters)

rot.compose(var, inplace=True)

# FIX: called num_parameters_settable() as a method -> use num_parameters property, because num_parameters counts all free parameters of the composed circuit (sum of both)
print(rot.num_parameters)

