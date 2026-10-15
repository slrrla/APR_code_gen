from qiskit.circuit.library import TwoLocal
from qiskit.circuit.library import iSwapGate

num_spin_orbitals = 4

ansatz = TwoLocal(
    num_spin_orbitals,
    ['ry', 'rz'],
    # FIX: entanglement block given as the unsupported string 'iswap' -> pass an iSwapGate() instance, because TwoLocal cannot resolve that name but accepts gate objects directly
    entanglement_blocks=iSwapGate(),
    entanglement='linear'
)

print(ansatz.decompose())
