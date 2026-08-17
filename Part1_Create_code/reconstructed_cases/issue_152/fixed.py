import numpy as np
from scipy.linalg import dft
from qiskit import *
from qiskit.circuit.library import QFT

n = 2
dft_matrix = (1/np.sqrt(2**n)) * dft(2**n)
# Qiskit's QFT uses omega = e^{+2pi i/n}, while scipy's dft uses omega = e^{-2pi i/n}.
# Use the inverse QFT so the conventions line up (they are complex conjugates of one another).
qft_matrix = execute(QFT(n, inverse=True), Aer.get_backend('unitary_simulator')).result().get_unitary()

# remove components almost zero for enhanced visualization
eps = 0.00001
dft_matrix.real[np.abs(dft_matrix.real) < eps] = 0
dft_matrix.imag[np.abs(dft_matrix.imag) < eps] = 0
qft_matrix.real[np.abs(qft_matrix.real) < eps] = 0
qft_matrix.imag[np.abs(qft_matrix.imag) < eps] = 0

print(dft_matrix, qft_matrix)
