# Fixed: use the correct class WeightedPauliOperator to build and Trotterize a Pauli sum.
from qiskit.aqua.operators import WeightedPauliOperator

pauli_dict = {
    'paulis': [
        {'coeff': {'imag': 0.0, 'real': 1.0}, 'label': 'ZZ'},
        {'coeff': {'imag': 0.0, 'real': 1.0}, 'label': 'XX'}
    ]
}

paulistring = WeightedPauliOperator.from_dict(pauli_dict)

qc_trotter = paulistring.evolve(evo_time=1, expansion_order=2)

print(qc_trotter)
