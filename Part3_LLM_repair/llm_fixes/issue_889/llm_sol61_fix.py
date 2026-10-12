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
    # FIX: The onsite term was eps*Z -> use eps*(I-Z)/2, because this is the Jordan-Wigner occupation operator.
    return PauliSumOp.from_list([('I' * N, eps / 2), (''.join(label), -eps / 2)])

def hopping_term(k, N):
    label = ['I'] * N
    label[k] = 'X'
    label[(k + 1) % N] = 'X'
    # FIX: The closing bond omitted its Jordan-Wigner string -> insert intermediate Z operators, because the endpoints are nonadjacent in the Jordan-Wigner ordering.
    if k == N - 1:
        label[1:N - 1] = ['Z'] * (N - 2)
    # FIX: Hopping used only t*XX -> use t*(XX+YY)/2 with the same Z string, because both terms are required for fermionic hopping.
    return PauliSumOp.from_list([(''.join(label), t / 2), (''.join(label).replace('X', 'Y'), t / 2)])

H = None
for k in range(N):
    term1 = onsite_term(k, N)
    term2 = hopping_term(k, N)
    H = term1 if H is None else H + term1
    H = H + term2

circ = QuantumCircuit(N)
# FIX: A Hamiltonian was appended as a gate -> append its time-evolution gate, because exp(-i*time_*H) is unitary and can be applied to the circuit.
circ.append((time_ * H).exp_i().to_circuit().to_gate(), list(range(N)))

