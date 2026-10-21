from qiskit.circuit.library import TwoLocal, iSwapGate

num_spin_orbitals = 4

# FIX: entanglement block given as the string 'iswap', which TwoLocal's name lookup does not resolve -> pass an iSwapGate instance, because TwoLocal accepts gate objects as entanglement blocks
ansatz = TwoLocal(
    num_spin_orbitals,
    ['ry', 'rz'],
    entanglement_blocks=iSwapGate(),
    entanglement='linear'
)

print(ansatz.decompose())
