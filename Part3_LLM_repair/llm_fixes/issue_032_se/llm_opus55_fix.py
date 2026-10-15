# FIX: iSwapGate was not imported -> added it to the import, because the gate object is needed instead of the unsupported string name
from qiskit.circuit.library import TwoLocal, iSwapGate

num_spin_orbitals = 4

ansatz = TwoLocal(
    num_spin_orbitals,
    ['ry', 'rz'],
    # FIX: 'iswap' string is not in TwoLocal's known layer names -> pass iSwapGate(), because TwoLocal accepts gate objects as entanglement blocks
    entanglement_blocks=iSwapGate(),
    entanglement='linear'
)

print(ansatz.decompose())
