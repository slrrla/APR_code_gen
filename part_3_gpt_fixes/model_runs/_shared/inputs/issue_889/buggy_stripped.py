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
    return PauliSumOp.from_list([(''.join(label), eps)])

def hopping_term(k, N):
    label = ['I'] * N
    label[k] = 'X'
    label[(k + 1) % N] = 'X'
    return PauliSumOp.from_list([(''.join(label), t)])

H = None
for k in range(N):
    term1 = onsite_term(k, N)
    term2 = hopping_term(k, N)
    H = term1 if H is None else H + term1
    H = H + term2

circ = QuantumCircuit(N)
circ.append(H, list(range(N)))
