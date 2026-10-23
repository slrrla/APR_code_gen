# FIX: The 'iswap' layer name is unsupported -> import iSwapGate, because TwoLocal accepts gate instances.
from qiskit.circuit.library import TwoLocal, iSwapGate

num_spin_orbitals = 4

ansatz = TwoLocal(
    num_spin_orbitals,
    ['ry', 'rz'],
    # FIX: The 'iswap' string fails layer lookup -> pass iSwapGate(), because it supplies the intended entangler directly.
    entanglement_blocks=iSwapGate(),
    entanglement='linear'
)

print(ansatz.decompose())

