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

# FIX: called num_parameters_settable() (blueprint-only count, a non-callable property) -> use num_parameters, because it counts all free parameters actually in the circuit
print(rot.num_parameters)

rot.compose(var, inplace=True)

# FIX: num_parameters_settable() ignores composed gates -> use num_parameters, because it includes the parameters added by compose (2 + 2 = 4)
print(rot.num_parameters)
