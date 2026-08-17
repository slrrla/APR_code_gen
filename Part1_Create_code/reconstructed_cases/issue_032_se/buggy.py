from qiskit.circuit.library import TwoLocal

num_spin_orbitals = 4

ansatz = TwoLocal(
    num_spin_orbitals,
    ['ry', 'rz'],
    entanglement_blocks='iswap',
    entanglement='linear'
)

print(ansatz.decompose())
