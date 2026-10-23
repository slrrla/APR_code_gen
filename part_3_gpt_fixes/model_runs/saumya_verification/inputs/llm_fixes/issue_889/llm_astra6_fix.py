import numpy as np
from qiskit import QuantumCircuit
# FIX: A Hamiltonian is not a circuit gate -> import PauliEvolutionGate, because it implements Hamiltonian time evolution.
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.opflow import PauliSumOp

N = 3
eps = 1.0
t = 0.5
time_ = 1.0

def onsite_term(k, N):
    label = ['I'] * N
    label[k] = 'Z'
    # FIX: The occupation operator was Z -> use (I - Z)/2, because this is the Jordan-Wigner image of c†c.
    return PauliSumOp.from_list([('I' * N, eps / 2), (''.join(label), -eps / 2)])

def hopping_term(k, N):
    label = ['I'] * N
    label[k] = 'X'
    label[(k + 1) % N] = 'X'
    # FIX: The closing bond omitted its Jordan-Wigner string -> insert intermediate Z operators, because fermionic hopping requires their parity.
    for j in range(min(k, (k + 1) % N) + 1, max(k, (k + 1) % N)):
        label[j] = 'Z'
    # FIX: XX alone is not number-conserving hopping -> use t(XX + YY)/2 with the parity string, because both Hermitian-conjugate hopping terms contribute.
    return PauliSumOp.from_list([(''.join(label), t / 2), (''.join(label).replace('X', 'Y'), t / 2)])

H = None
for k in range(N):
    term1 = onsite_term(k, N)
    term2 = hopping_term(k, N)
    H = term1 if H is None else H + term1
    H = H + term2

circ = QuantumCircuit(N)
# FIX: PauliSumOp cannot be appended as a gate -> append its evolution gate, because the circuit must apply exp(-i H time_) rather than H.
circ.append(PauliEvolutionGate(H, time=time_), list(range(N)))

