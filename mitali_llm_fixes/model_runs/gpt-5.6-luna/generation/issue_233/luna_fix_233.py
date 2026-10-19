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

# FIX: composing into a TwoLocal blueprint leaves its settable-parameter count stale -> decompose before composing, because a regular QuantumCircuit tracks parameters added by composition
rot = rot.decompose()
rot.compose(var, inplace=True)

print(rot.num_parameters_settable())
