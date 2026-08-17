# Same illustrative QPE circuit; no code correction applies since the
# original question and answer were purely conceptual (explaining the
# tensor-product-to-superposition identity used in QPE derivations).

from qiskit import QuantumCircuit, QuantumRegister, execute
from qiskit import BasicAer
import numpy as np

n = 3  # number of counting qubits
theta = 1/4  # phase to estimate

qpe = QuantumCircuit(n+1, n)

# Prepare eigenstate |1> on the target qubit
qpe.x(n)

for qubit in range(n):
    qpe.h(qubit)

# Apply controlled phase rotations e^{2 pi i theta 2^j}
for qubit in range(n):
    qpe.cp(2*np.pi*theta*2**qubit, qubit, n)

qpe.barrier()

# Inverse QFT
for j in range(n):
    for k in range(j):
        qpe.cp(-np.pi/float(2**(j-k)), k, j)
    qpe.h(j)

qpe.barrier()
for i in range(n):
    qpe.measure(i, i)

backend = BasicAer.get_backend('qasm_simulator')
result = execute(qpe, backend, shots=1024).result()
counts = result.get_counts()
print(counts)
