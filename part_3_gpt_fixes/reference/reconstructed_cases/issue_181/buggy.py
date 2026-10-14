# Importing standard Qiskit libraries and configuring account
from qiskit import QuantumCircuit, execute, Aer, IBMQ
import numpy as np
from qiskit.compiler import transpile, assemble

# HHL in Qiskit
from qiskit.aqua.algorithms import HHL

matrix_A = np.array([[1.5, 0.5], [0.5, 1.5]])
vector_b = [0.9010, -0.4339]
# x = [0.8184, -0.5747] #expected result

backend = Aer.get_backend('statevector_simulator')

# num_q - Number of qubits required for the matrix Operator instance
# num_a - Number of ancillary qubits for Eigenvalues instance
hhlObject = HHL(matrix=matrix_A, vector=vector_b, quantum_instance=backend, num_q=2, num_a=1)

res = hhlObject.run(quantum_instance=backend)
print(res)
