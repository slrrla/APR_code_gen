from qiskit.circuit.library import TwoLocal
from qiskit import QuantumCircuit
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

# FIX: composing in place into a BlueprintCircuit (TwoLocal) -> first copy rot into a plain QuantumCircuit, because the blueprint rebuilds itself and discards the composed gates, while a regular circuit keeps them
rot = QuantumCircuit(rot.num_qubits).compose(rot)
rot.compose(var, inplace=True)

print(rot.num_parameters_settable())
