import numpy as np
from qiskit import QuantumCircuit
from qiskit.opflow import PauliSumOp
from qiskit.circuit.library import PauliEvolutionGate  # FIX: missing import for wrapping the Hamiltonian as a gate -> added import, because PauliEvolutionGate is needed to append a PauliSumOp to a circuit

N = 3
eps = 1.0
t = 0.5
time_ = 1.0

def onsite_term(k, N):
    label = ['I'] * N
    label[k] = 'Z'
    return PauliSumOp.from_list([(''.join(label), eps)])

def hopping_term(k, N):
    # FIX: hopping only had XX with coefficient t -> added YY and changed coefficient to t/2, because Jordan-Wigner gives c_i^† c_{i+1} + h.c. = (XX + YY)/2
    label_xx = ['I'] * N
    label_xx[k] = 'X'
    label_xx[(k + 1) % N] = 'X'
    label_yy = ['I'] * N
    label_yy[k] = 'Y'
    label_yy[(k + 1) % N] = 'Y'
    return PauliSumOp.from_list([(''.join(label_xx), t / 2), (''.join(label_yy), t / 2)])

H = None
for k in range(N):
    term1 = onsite_term(k, N)
    term2 = hopping_term(k, N)
    H = term1 if H is None else H + term1
    H = H + term2

circ = QuantumCircuit(N)
# FIX: circ.append(H, ...) appended a PauliSumOp directly, which is not a circuit instruction -> wrap H in PauliEvolutionGate with time_, because this turns the Hamiltonian into an appendable gate exp(-i H t)
circ.append(PauliEvolutionGate(H.primitive, time=time_), list(range(N)))
