import numpy as np
from qiskit.quantum_info import Statevector

try:
    from qiskit.opflow import PauliSumOp
    O = PauliSumOp.from_list([
        ("II", -1),
        ("IZ", 0.4),
        ("ZI", -0.4),
        ("ZZ", -1),
        ("XX", 0.1),
    ])
except ImportError:
    from qiskit.quantum_info import SparsePauliOp
    O = SparsePauliOp.from_list([
        ("II", -1),
        ("IZ", 0.4),
        ("ZI", -0.4),
        ("ZZ", -1),
        ("XX", 0.1),
    ])

psi = (
    Statevector.from_label("00") +
    Statevector.from_label("11")
) / np.sqrt(2)

# Bug: computes <psi|O|psi>, not <psi|O^2|psi>
operator_matrix = O.to_matrix()
expectation_value = psi.expectation_value(operator_matrix)

print(expectation_value)
