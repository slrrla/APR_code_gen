import numpy as np
from qiskit import QuantumCircuit
from qiskit.opflow import PauliSumOp

N = 3
eps = 1.0
t = 0.5
time_ = 1.0

# FIX: onsite term used eps*Z, but n_k = (I - Z_k)/2 -> return eps/2 * I - eps/2 * Z, because the number operator is (I - Z)/2 under Jordan-Wigner
def onsite_term(k, N):
    label = ['I'] * N
    label[k] = 'Z'
    return PauliSumOp.from_list([('I' * N, eps / 2), (''.join(label), -eps / 2)])

# FIX: hopping term used only X_k X_{k+1}, but c_k^dag c_{k+1} + h.c. = (X_k X_{k+1} + Y_k Y_{k+1})/2 -> add the YY term with coefficient t/2 each, because the Jordan-Wigner hopping needs both XX and YY parts
def hopping_term(k, N):
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
circ.append(H, list(range(N)))
