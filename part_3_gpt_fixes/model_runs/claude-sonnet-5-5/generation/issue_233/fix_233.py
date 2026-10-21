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

# FIX: in-place compose on a lazily built BlueprintCircuit kept only one block's parameters -> compose into a new plain QuantumCircuit and count its parameters, because a plain circuit tracks parameters from both composed circuits
rot = rot.compose(var)

print(rot.num_parameters)
