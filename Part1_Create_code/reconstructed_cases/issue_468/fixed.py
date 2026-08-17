from qiskit.aqua.operators.legacy import commutator
from qiskit.aqua.operators import WeightedPauliOperator
from qiskit.quantum_info import Pauli

pauli_a = 'X'
pauli_b = 'Z'
coeff_a = 0.5
coeff_b = 0.5

pauli_term_a = [coeff_a, Pauli.from_label(pauli_a)]
pauli_term_b = [coeff_b, Pauli.from_label(pauli_b)]

op_a = WeightedPauliOperator(paulis=[pauli_term_a])
op_b = WeightedPauliOperator(paulis=[pauli_term_b])

print(commutator(op_a, op_b))
