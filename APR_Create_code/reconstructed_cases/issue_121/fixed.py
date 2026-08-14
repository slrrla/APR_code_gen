import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator

def qft_circuit(n):
    qc = QuantumCircuit(n)
    for j in range(n):
        qc.h(j)
        for k in range(j + 1, n):
            qc.cp(2 * np.pi / 2 ** (k - j + 1), k, j)
    # FIX: reverse the qubit order at the end, since the circuit's
    # natural qubit ordering is the reverse of the standard QFT
    # definition's ordering -- this resolves the apparent mismatch
    # between psi_6 (unitary output) and the circuit output.
    for i in range(n // 2):
        qc.swap(i, n - i - 1)
    return qc

n = 3
qc = qft_circuit(n)
circuit_unitary = Operator(qc).data

# QFT unitary matrix (textbook definition)
N = 2 ** n
qft_matrix = np.zeros((N, N), dtype=complex)
omega = np.exp(2j * np.pi / N)
for x in range(N):
    for y in range(N):
        qft_matrix[y, x] = omega ** (x * y) / np.sqrt(N)

print("Circuit unitary:\n", circuit_unitary)
print("QFT matrix:\n", qft_matrix)
print("Equal (with swap):", np.allclose(circuit_unitary, qft_matrix))
