# FIX: import the iSWAP gate class -> import iSwapGate, because TwoLocal does not recognize "iswap" as a layer name
from qiskit.circuit.library import TwoLocal, iSwapGate

num_spin_orbitals = 4

ansatz = TwoLocal(
    num_spin_orbitals,
    ['ry', 'rz'],
    # FIX: pass an iSWAP gate instance -> iSwapGate(), because TwoLocal accepts gate objects even though "iswap" is not a recognized layer name
    entanglement_blocks=iSwapGate(),
    entanglement='linear'
)

print(ansatz.decompose())
