# FIX: 'iswap' string is not in TwoLocal's layer-name lookup -> import iSwapGate so a gate instance can be passed, because TwoLocal accepts Instruction objects directly as entanglement blocks
from qiskit.circuit.library import TwoLocal, iSwapGate

num_spin_orbitals = 4

ansatz = TwoLocal(
    num_spin_orbitals,
    ['ry', 'rz'],
    # FIX: entanglement_blocks='iswap' (string) -> iSwapGate() instance, because the string name is not recognized while a gate object is accepted as a block
    entanglement_blocks=iSwapGate(),
    entanglement='linear'
)

print(ansatz.decompose())
