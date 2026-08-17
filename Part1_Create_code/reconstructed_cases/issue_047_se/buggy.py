# Buggy attempt: trying to Trotterize a Pauli sum using a misspelled/incorrect class name.
from qiskit.aqua.operators import WightedPauliSum  # NOTE: typo - this class does not exist in qiskit.aqua.operators

pauli_dict = {
    'paulis': [
        {'coeff': {'imag': 0.0, 'real': 1.0}, 'label': 'ZZ'},
        {'coeff': {'imag': 0.0, 'real': 1.0}, 'label': 'XX'}
    ]
}

paulistring = WightedPauliSum.from_dict(pauli_dict)

qc_trotter = paulistring.evolve(evo_time=1, expansion_order=2)

print(qc_trotter)
