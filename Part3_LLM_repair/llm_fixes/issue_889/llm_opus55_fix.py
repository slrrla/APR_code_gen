import numpy as np
from qiskit import QuantumCircuit
# FIX: deprecated/removed opflow PauliSumOp -> SparsePauliOp and PauliEvolutionGate, because opflow is removed in Qiskit 1.0 and an operator must be turned into an evolution gate
from qiskit.quantum_info import SparsePauliOp
from qiskit.circuit.library import PauliEvolutionGate

N = 3
eps = 1.0
t = 0.5
time_ = 1.0

def onsite_term(k, N):
    label = ['I'] * N
    label[k] = 'Z'
    # FIX: PauliSumOp.from_list -> SparsePauliOp.from_list, because opflow no longer exists
    return SparsePauliOp.from_list([(''.join(label), eps)])

def hopping_term(k, N):
    label = ['I'] * N
    label[k] = 'X'
    label[(k + 1) % N] = 'X'
    # FIX: PauliSumOp.from_list -> SparsePauliOp.from_list, because opflow no longer exists
    return SparsePauliOp.from_list([(''.join(label), t)])

H = None
for k in range(N):
    term1 = onsite_term(k, N)
    term2 = hopping_term(k, N)
    H = term1 if H is None else H + term1
    H = H + term2

circ = QuantumCircuit(N)
# FIX: appending the raw operator H -> appending PauliEvolutionGate(H, time=time_), because a circuit needs a gate (exp(-iHt)), not a Hamiltonian
circ.append(PauliEvolutionGate(H, time=time_), list(range(N)))
