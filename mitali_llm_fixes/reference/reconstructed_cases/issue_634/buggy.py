from qiskit import QuantumRegister, ClassicalRegister
from qiskit import QuantumCircuit
import numpy as np

q = QuantumRegister(1, 'q')
c = ClassicalRegister(1, 'c')
circuit = QuantumCircuit(q, c)
A = circuit.rx(np.pi/2, q[0])
circuit.rx(np.pi/2, A)
circuit.measure(q, c)
print(circuit)
