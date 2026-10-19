import numpy as np
from qiskit import QuantumCircuit

# Build the circuit with the default qubit ordering [0,1,2,3,4]
quanc = QuantumCircuit(5)
quanc.crz(np.pi, 1, 0)
quanc.cx(1, [i for i in range(2, 5)])

print(quanc)
