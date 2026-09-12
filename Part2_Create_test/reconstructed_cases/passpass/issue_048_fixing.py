import qiskit
import math
from qiskit import QuantumCircuit

circuit = QuantumCircuit(2)

# a) crz with positional arguments
circuit.crz(math.pi/2, 0, 1)

# b) cp replaces deprecated cu1
circuit.cp(math.pi/2, 0, 1)

print(circuit)
