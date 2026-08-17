import matplotlib.pyplot as plt
import numpy as np
import math
from qiskit import *
import qiskit

circuit = QuantumCircuit(9)

# Initialize qubit 0 to an arbitrary state drawn from the Haar measure
sv = qiskit.quantum_info.random_statevector(2)
circuit.initialize(sv.data, 0)

circuit.cnot(0, 3)
circuit.cnot(0, 6)
circuit.h(0)
circuit.h(3)
circuit.h(6)
circuit.cnot(0, 1)
circuit.cnot(3, 4)
circuit.cnot(6, 7)
circuit.cnot(0, 2)
circuit.cnot(3, 5)
circuit.cnot(6, 8)

# Insert some error here
circuit.barrier()
circuit.x(0)
circuit.id(1)
circuit.id(2)
circuit.id(3)
circuit.id(4)
circuit.id(5)
circuit.id(6)
circuit.id(7)
circuit.id(8)
circuit.barrier()

circuit.cnot(0, 1)
circuit.cnot(3, 4)
circuit.cnot(6, 7)
circuit.cnot(0, 2)
circuit.cnot(3, 5)
circuit.cnot(6, 8)
circuit.ccx(2, 1, 0)
circuit.ccx(5, 4, 3)
circuit.ccx(8, 7, 6)
circuit.h(0)
circuit.h(3)
circuit.h(6)
circuit.cnot(0, 3)
circuit.cnot(0, 6)
circuit.ccx(8, 3, 0)

circuit.draw(output='mpl')
plt.show()

# Run the quantum circuit on a statevector simulator backend
backend = Aer.get_backend('statevector_simulator')

# Create a Quantum Program for execution
job = backend.run(circuit)
result = job.result()
outputstate = result.get_statevector(circuit, decimals=3)
print(outputstate)
