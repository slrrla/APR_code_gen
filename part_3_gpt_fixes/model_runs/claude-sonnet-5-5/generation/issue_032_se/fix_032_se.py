from qiskit.circuit.library import TwoLocal, iSwapGate

num_spin_orbitals = 4

ansatz = TwoLocal(
    num_spin_orbitals,
    ['ry', 'rz'],
    # FIX: 'iswap' string is not a recognized TwoLocal layer name -> pass iSwapGate() instance, because TwoLocal accepts gate objects as blocks and only a fixed set of names as strings
    entanglement_blocks=iSwapGate(),
    entanglement='linear'
)

print(ansatz.decompose())
