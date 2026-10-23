# FIX: iSwap is not recognized as a string layer name -> import its gate class, because TwoLocal accepts gate objects.
from qiskit.circuit.library import TwoLocal, iSwapGate

num_spin_orbitals = 4

ansatz = TwoLocal(
    num_spin_orbitals,
    ['ry', 'rz'],
    # FIX: the string 'iswap' is not recognized -> pass an iSwapGate instance, because TwoLocal accepts gate objects.
    entanglement_blocks=iSwapGate(),
    entanglement='linear'
)

print(ansatz.decompose())

