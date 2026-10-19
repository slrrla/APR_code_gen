from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
import numpy as np

n = 2
circuit = QuantumCircuit(n, n)

# Create a Statevector directly from a binary label instead of a
# manually constructed amplitude vector
sv = Statevector.from_label('11')

# Define rest of the circuit
circuit.measure(range(n), range(n))

# Apply the circuit to the statevector
sv = sv.evolve(circuit)

print(sv.data)
