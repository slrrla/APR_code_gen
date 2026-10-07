from qiskit.quantum_info import Statevector
from qiskit.circuit.library import GroverOperator
from qiskit import QuantumCircuit
import numpy as np

# Desired marked (solution) states for the oracle
targets = ['101', '110']

# Create an oracle circuit that marks multiple states with a phase flip
# We need to construct a circuit that applies phase -1 to target states
n_qubits = len(targets[0])

# Create a statevector oracle for multiple marked states
# We'll create a statevector where the target states have -1 phase
data = np.zeros(2**n_qubits, dtype=complex)
for target in targets:
    idx = int(target, 2)  # Convert binary string to integer index
    data[idx] = -1  # Phase flip for target states

# Normalize the statevector
data = data / np.linalg.norm(data)

oracle = Statevector(data)

grover_op = GroverOperator(oracle)
print(grover_op)
