import qiskit
import numpy as np
from qiskit.quantum_info.operators import Operator

circuit = qiskit.QuantumCircuit(3)
circuit.swap(0, 1)
circuit.swap(1, 2)

print(Operator(circuit).data)
print({x: y for (x, y) in zip(*np.nonzero(Operator(circuit).data))})
