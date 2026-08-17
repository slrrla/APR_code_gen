# Correct way to apply the projector pi = [[1,0],[0,0]] to qubit 0
# of an arbitrary state: extract the statevector, build the projector
# (tensored with identity on the other qubits, respecting Qiskit's
# reversed qubit ordering), apply it via matrix multiplication,
# renormalize, and reinitialize a new circuit with the result.

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
import numpy as np

# Bell state |psi> = (|00> + |11>)/sqrt(2)
qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)

statevector = np.array(Statevector(qc))

# Projector onto |0> for qubit 0
pi = np.array([[1, 0], [0, 0]])
identity = np.eye(2)

# Qiskit statevector uses reversed (little-endian) qubit ordering,
# so the identity for qubit 1 goes on the left of the kron product.
projector = np.kron(identity, pi)

statevector = np.matmul(projector, statevector)
norm = np.linalg.norm(statevector)
statevector = statevector / norm

Number_of_qubits = 2
qc = QuantumCircuit(Number_of_qubits)
qc.initialize(list(statevector), qc.qubits)

print(Statevector(qc))
