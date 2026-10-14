# Quantum Phase Estimation with correctly ordered inverse QFT (with swaps)
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, Aer, execute
import numpy as np

n = 3  # number of counting qubits
theta = 1/3  # phase to estimate

qpe = QuantumCircuit(n+1, n)

# Prepare eigenstate on the last qubit
qpe.x(n)

# Apply Hadamards on counting qubits
for qubit in range(n):
    qpe.h(qubit)

# Controlled phase rotations
repetitions = 1
for counting_qubit in range(n):
    for i in range(repetitions):
        qpe.cp(2*np.pi*theta, counting_qubit, n)
    repetitions *= 2

# Correct inverse QFT: swap qubits first, then apply controlled phases and Hadamards
def qft_dagger(circuit, n):
    for qubit in range(n//2):
        circuit.swap(qubit, n-qubit-1)
    for j in range(n):
        for m in range(j):
            circuit.cp(-np.pi/float(2**(j-m)), m, j)
        circuit.h(j)

qft_dagger(qpe, n)

qpe.measure(range(n), range(n))

backend = Aer.get_backend('qasm_simulator')
counts = execute(qpe, backend, shots=1024).result().get_counts()
print(counts)
