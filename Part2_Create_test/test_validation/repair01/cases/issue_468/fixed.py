from qiskit.aqua.operators.legacy import commutator
from qiskit.aqua.operators import WeightedPauliOperator
from qiskit.quantum_info import Pauli

# Preserve the original density matrices: X|0><0|X and Z|0><0|Z.
op_a = WeightedPauliOperator(paulis=[
    [0.5, Pauli.from_label('I')], [-0.5, Pauli.from_label('Z')]])
op_b = WeightedPauliOperator(paulis=[
    [0.5, Pauli.from_label('I')], [0.5, Pauli.from_label('Z')]])

print(commutator(op_a, op_b))
