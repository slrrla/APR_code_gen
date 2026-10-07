from qiskit.circuit.library import TwoLocal, iSwapGate

num_spin_orbitals = 4

ansatz = TwoLocal(
    num_spin_orbitals,
    ['ry', 'rz'],
    entanglement_blocks=iSwapGate(),
    entanglement='linear'
)

print(ansatz.decompose())
