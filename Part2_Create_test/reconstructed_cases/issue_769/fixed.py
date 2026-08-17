from inspect import getmembers, isclass
import numpy as np
from qiskit.circuit.library import standard_gates


def get_qiskit_gate(u):
    for name, gate in getmembers(standard_gates, isclass):
        try:
            unitary = gate().__array__()
        except Exception:
            continue
        if unitary.shape == u.shape and np.allclose(unitary, u):
            return name
    return None


unitary = np.array([[0, 1], [1, 0]])
print(get_qiskit_gate(u=unitary))
