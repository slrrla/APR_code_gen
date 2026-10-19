import numpy as np
from qiskit import QuantumCircuit
from qiskit.opflow import PauliSumOp

N = 3
eps = 1.0
t = 0.5
time_ = 1.0

def onsite_term(k, N):
    label = ['I'] * N
    label[k] = 'Z'
    # FIX: occupation was represented by Z -> use (I - Z)/2, because this equals sigma_minus times sigma_plus.
    return PauliSumOp.from_list([('I' * N, eps / 2), (''.join(label), -eps / 2)])

def hopping_term(k, N):
    label = ['I'] * N
    label[k] = 'X'
    label[(k + 1) % N] = 'X'
    # FIX: hopping contained only XX -> include XX and YY with intervening Z operators, because Jordan-Wigner hopping requires both components and a parity string across the closing bond.
    for j in range(min(k, (k + 1) % N) + 1, max(k, (k + 1) % N)):
        label[j] = 'Z'
    return PauliSumOp.from_list([(''.join(label), t / 2), (''.join(label).replace('X', 'Y'), t / 2)])

H = None
for k in range(N):
    term1 = onsite_term(k, N)
    term2 = hopping_term(k, N)
    H = term1 if H is None else H + term1
    H = H + term2

circ = QuantumCircuit(N)
# FIX: a Hamiltonian is not a circuit instruction -> append its time-evolution instruction, because the gate implements exp(-i * time_ * H).
circ.append((time_ * H).exp_i().to_instruction(), list(range(N)))
