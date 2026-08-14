import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute, Aer

# Example Hermitian operator A = sigma_z (x) sigma_z acting on 2 qubits.
A = np.array([[1, 0, 0, 0],
              [0, -1, 0, 0],
              [0, 0, -1, 0],
              [0, 0, 0, 1]])

# Diagonalize A: A = U^dagger * Lambda * U
eigvals, eigvecs = np.linalg.eigh(A)
U = eigvecs.conj().T  # change-of-basis unitary

q = QuantumRegister(2)
c = ClassicalRegister(2)
qc = QuantumCircuit(q, c)

# some arbitrary state preparation
qc.h(q[0])
qc.cx(q[0], q[1])

# apply the unitary that rotates into the eigenbasis of A before measuring
qc.unitary(U, [q[0], q[1]], label='U')

qc.measure(q, c)

backend = Aer.get_backend('qasm_simulator')
shots = 1024
result = execute(qc, backend, shots=shots).result()
counts = result.get_counts()

probs = sorted([(i, cnt / shots) for i, cnt in counts.items()])
P = np.float64(np.array(probs)[:, 1])

# expectation value reconstructed from eigenvalues and measured probabilities
A_expectation = eigvals @ P
print(A_expectation)
