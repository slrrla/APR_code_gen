import numpy as np
from qiskit.chemistry import FermionicOperator

def ssh_ham(gamma, lamda, n):
    sigmax = np.array([[0, 1], [1, 0]], dtype=np.complex_)
    sigmay = np.array([[0, -1j], [1j, 0]], dtype=np.complex_)
    op_eye_x = np.eye(n)
    op_cos_x = 1/2 * (np.eye(n, k=1) + np.eye(n, k=-1))
    op_sin_x = 1j/2 * (np.eye(n, k=1) - np.eye(n, k=-1))
    h = np.kron(gamma*op_eye_x + lamda*op_cos_x, sigmax) + np.kron(lamda*op_sin_x, sigmay)
    return h

fer_op = FermionicOperator(h1=ssh_ham(1, 2, 10))
