import numpy as np
from qiskit.circuit.library import RZZGate, RXXGate, RYYGate

theta = 0.7

def rz(t):
    return np.array([[np.exp(-1j*t/2), 0], [0, np.exp(1j*t/2)]])

def rx(t):
    return np.array([[np.cos(t/2), -1j*np.sin(t/2)],
                      [-1j*np.sin(t/2), np.cos(t/2)]])

def ry(t):
    return np.array([[np.cos(t/2), -np.sin(t/2)],
                      [np.sin(t/2), np.cos(t/2)]])

P0 = np.array([[1, 0], [0, 0]])
P1 = np.array([[0, 0], [0, 1]])

# RZZ: computational-basis (|0>,|1>) decomposition, unchanged.
rzz_decomp = np.kron(P0, rz(theta)) + np.kron(P1, rz(-theta))
rzz_matrix = RZZGate(theta).to_matrix()
print("RZZ decomposition matches:", np.allclose(rzz_decomp, rzz_matrix))

# RXX must be decomposed in the |+>,|-> eigenbasis of sigma_x, not the
# computational basis, since RXX and RZZ are related by a change of basis.
plus = (1/np.sqrt(2)) * np.array([[1], [1]])
minus = (1/np.sqrt(2)) * np.array([[1], [-1]])
Pplus = plus @ plus.conj().T
Pminus = minus @ minus.conj().T

rxx_decomp = np.kron(Pplus, rx(theta)) + np.kron(Pminus, rx(-theta))
rxx_matrix = RXXGate(theta).to_matrix()
print("RXX decomposition matches:", np.allclose(rxx_decomp, rxx_matrix))

# RYY must be decomposed in the |+i>,|-i> eigenbasis of sigma_y.
plus_i = (1/np.sqrt(2)) * np.array([[1], [1j]])
minus_i = (1/np.sqrt(2)) * np.array([[1], [-1j]])
Pplus_i = plus_i @ plus_i.conj().T
Pminus_i = minus_i @ minus_i.conj().T

ryy_decomp = np.kron(Pplus_i, ry(theta)) + np.kron(Pminus_i, ry(-theta))
ryy_matrix = RYYGate(theta).to_matrix()
print("RYY decomposition matches:", np.allclose(ryy_decomp, ryy_matrix))
