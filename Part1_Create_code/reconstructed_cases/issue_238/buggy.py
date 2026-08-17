import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute, Aer

# Example Hermitian operator A = sigma_z (x) sigma_z acting on 2 qubits.
# In general A need not be diagonal in the computational basis.
A = np.array([[1, 0, 0, 0],
              [0, -1, 0, 0],
              [0, 0, -1, 0],
              [0, 0, 0, 1]])

q = QuantumRegister(2)
c = ClassicalRegister(2)
qc = QuantumCircuit(q, c)

# some arbitrary state preparation
qc.h(q[0])
qc.cx(q[0], q[1])

# BUG: measuring directly in the computational basis and treating the
# resulting probabilities as if they already correspond to the
# eigenbasis of A, without ever diagonalizing A or applying the
# change-of-basis unitary to the circuit.
qc.measure(q, c)

backend = Aer.get_backend('qasm_simulator')
shots = 1024
result = execute(qc, backend, shots=shots).result()
counts = result.get_counts()

probs = sorted([(i, cnt / shots) for i, cnt in counts.items()])
P = np.float64(np.array(probs)[:, 1])

# incorrectly assumes the diagonal of A gives the eigenvalues in the
# same ordering as the measured computational-basis probabilities
A_expectation = np.diag(A) @ P
print(A_expectation)
