import numpy as np
import scipy as sp
from qiskit import QuantumCircuit, execute, Aer

def random_unitary(N):
    """ Return a Haar distributed random unitary from U(N) """
    Z = np.random.randn(N, N) + 1.0j * np.random.randn(N, N)
    [Q, R] = sp.linalg.qr(Z)
    D = np.diag(np.diagonal(R) / np.abs(np.diagonal(R)))
    return np.dot(Q, D)

def haar_integral(num_qubits, samples):
    """ Return calculation of Haar Integral for a specified number of samples. """
    N = 2**num_qubits
    randunit_density = np.zeros((N, N), dtype=complex)
    zero_state = np.zeros(N, dtype=complex)
    zero_state[0] = 1
    for _ in range(samples):
        A = np.matmul(zero_state, random_unitary(N)).reshape(-1, 1)
        randunit_density += np.kron(A, A.conj().T)
    randunit_density /= samples
    return randunit_density

def pqc_integral(num_qubits, ansatze, size, samples):
    """ Return calculation of Integral for a PQC over the uniformly sampled the parameters theta for the specified number of samples. """
    N = num_qubits
    randunit_density = np.zeros((2**N, 2**N), dtype=complex)
    for _ in range(samples):
        params = np.random.uniform(-np.pi, np.pi, size)
        ansatz = ansatze(params, N)
        result = execute(ansatz, backend=Aer.get_backend('statevector_simulator')).result()
        U = result.get_statevector(ansatz, decimals=5).reshape(-1, 1)
        randunit_density += np.kron(U, U.conj().T)
    return randunit_density / samples

def ansatz2(params, num_qubits):
    params = np.array(params).reshape(1)
    ansatz = QuantumCircuit(num_qubits, num_qubits)
    ansatz.h(0)
    ansatz.cx(0, 1)
    ansatz.rx(params[0], 0)
    return ansatz

print(np.linalg.norm(haar_integral(2, 2048) - pqc_integral(2, ansatz2, 1, 2048)))
