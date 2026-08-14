# import the necessary libraries
import math as m
from qiskit import *
from qiskit import BasicAer
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, execute
from qiskit_quantum_knn.encoding import analog
from numpy import linalg as LA
from scipy.spatial import distance

# First step is to encode the data into quantum states.
# There are some techniques to do it, in this case Amplitude embedding was used.
A = [2, 9, 8, 5, 4, 18, 16, 10]
B = [7, 5, 10, 3, 14, 10, 20, 6]

A_norm = LA.norm(A)
B_norm = LA.norm(B)
Dist = distance.euclidean(A, B)
Z = round(A_norm**2 + B_norm**2)

# create phi and psi state with the data
phi = [A_norm / m.sqrt(Z), -B_norm / m.sqrt(Z)]
psi = []
for i in range(len(A)):
    psi.append((A[i] / A_norm) / m.sqrt(2))
    psi.append((B[i] / B_norm) / m.sqrt(2))

# Quantum Circuit
q1 = QuantumRegister(1, name='q1')
q2 = QuantumRegister(1, name='q2')
q3 = QuantumRegister(4, name='q3')
c = ClassicalRegister(1, name='c')
qc = QuantumCircuit(q1, q2, q3, c)

# states initialization
qc.initialize(phi, q2[0])
qc.initialize(psi, q3[0:4])

# The swap test operator
qc.h(q1[0])
qc.cswap(q1[0], q2[0], q3[0])
qc.h(q1[0])
qc.measure(q1, c)

## Results
shots = 1000000
job = execute(qc, Aer.get_backend('qasm_simulator'), shots=shots)
job_result = job.result()
counts = job_result.get_counts(qc)
x = abs(((counts['0'] / shots - 0.5) / 0.5) * 2 * Z)
Q_Dist = round(m.sqrt(x), 4)
print('Quantum Distance: ', round(Q_Dist, 3))
print('Euclidean Distance: ', round(Dist, 3))
