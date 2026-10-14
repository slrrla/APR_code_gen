# import the necessary libraries
import math as m
import random
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, execute
from qiskit import Aer
from numpy import linalg as LA
from scipy.spatial import distance

# The original circuit only compares a single pair of vectors (A, B) using a
# SWAP test. As explained in the answer, trying to encode a whole set of
# candidate vectors {phi_i} into one circuit (via an extra index register and
# a W-oracle) does not actually give any quantum advantage: the resulting
# joint distribution p(i,0) is exactly reproducible by classically sampling
# an index i uniformly at random and then running the *same* standard SWAP
# test between psi and phi_i. So the "fix" is simply to reuse the existing
# pairwise SWAP-test code, but call it with a randomly sampled candidate
# vector instead of trying to build a single circuit for all vectors at once.

def swap_test_distance(A, B, shots=1000000):
    A_norm = LA.norm(A)
    B_norm = LA.norm(B)
    Dist = distance.euclidean(A, B)
    Z = round(A_norm**2 + B_norm**2)

    phi = [A_norm / m.sqrt(Z), -B_norm / m.sqrt(Z)]
    psi = []
    for i in range(len(A)):
        psi.append((A[i] / A_norm) / m.sqrt(2))
        psi.append((B[i] / B_norm) / m.sqrt(2))

    q1 = QuantumRegister(1, name='q1')
    q2 = QuantumRegister(1, name='q2')
    q3 = QuantumRegister(4, name='q3')
    c = ClassicalRegister(1, name='c')
    qc = QuantumCircuit(q1, q2, q3, c)

    qc.initialize(phi, q2[0])
    qc.initialize(psi, q3[0:4])

    qc.h(q1[0])
    qc.cswap(q1[0], q2[0], q3[0])
    qc.h(q1[0])
    qc.measure(q1, c)

    job = execute(qc, Aer.get_backend('qasm_simulator'), shots=shots)
    job_result = job.result()
    counts = job_result.get_counts(qc)
    x = abs(((counts.get('0', 0) / shots - 0.5) / 0.5) * 2 * Z)
    Q_Dist = round(m.sqrt(x), 4)
    return Q_Dist, round(Dist, 3)

# fixed reference vector psi
psi_vec = [7, 5, 10, 3, 14, 10, 20, 6]

# set of candidate vectors {phi_i}
vectors = [
    [2, 9, 8, 5, 4, 18, 16, 10],
    [7, 5, 10, 3, 14, 10, 20, 6],
    [1, 3, 5, 7, 9, 11, 13, 15],
]

# instead of building one big multi-vector circuit, randomly sample an
# index i and perform the standard pairwise SWAP test between psi and phi_i
i = random.randrange(len(vectors))
phi_i = vectors[i]

Q_Dist, Dist = swap_test_distance(phi_i, psi_vec)
print('Sampled vector index:', i)
print('Quantum Distance: ', Q_Dist)
print('Euclidean Distance: ', Dist)
