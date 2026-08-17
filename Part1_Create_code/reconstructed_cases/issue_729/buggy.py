import numpy as np
from qiskit.circuit.library import RZZGate, RXXGate

theta = 0.7

# The user believes any parametric multi-qubit unitary can be written as
# sum_k lambda_k * (W_1 (x) W_2) using computational-basis projectors,
# by analogy with RZZ(theta) = |0><0| (x) Rz(theta) + |1><1| (x) Rz(-theta).
def rz(t):
    return np.array([[np.exp(-1j*t/2), 0], [0, np.exp(1j*t/2)]])

P0 = np.array([[1, 0], [0, 0]])
P1 = np.array([[0, 0], [0, 1]])

rzz_decomp = np.kron(P0, rz(theta)) + np.kron(P1, rz(-theta))
rzz_matrix = RZZGate(theta).to_matrix()
print("RZZ decomposition matches:", np.allclose(rzz_decomp, rzz_matrix))

# Naively applying the same computational-basis projector trick to RXX,
# using Rx instead of Rz -- this does NOT reproduce RXX(theta).
def rx(t):
    return np.array([[np.cos(t/2), -1j*np.sin(t/2)],
                      [-1j*np.sin(t/2), np.cos(t/2)]])

rxx_decomp_wrong = np.kron(P0, rx(theta)) + np.kron(P1, rx(-theta))
rxx_matrix = RXXGate(theta).to_matrix()
print("RXX decomposition matches:", np.allclose(rxx_decomp_wrong, rxx_matrix))
