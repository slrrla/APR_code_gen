from qiskit.circuit.library import TwoLocal
# FIX: iSwapGate was not imported -> import it, because the block must be passed as a gate object
from qiskit.circuit.library import iSwapGate

num_spin_orbitals = 4

ansatz = TwoLocal(
    num_spin_orbitals,
    ['ry', 'rz'],
    # FIX: string 'iswap' is not a recognized layer name -> pass iSwapGate(), because TwoLocal accepts Instruction objects directly as blocks
    entanglement_blocks=iSwapGate(),
    entanglement='linear'
)

print(ansatz.decompose())
