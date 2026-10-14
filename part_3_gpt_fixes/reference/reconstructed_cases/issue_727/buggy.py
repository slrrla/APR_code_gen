import numpy
from math import pi
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit import Parameter

k = Parameter('k')

# Build a sub-circuit
q = QuantumRegister(2)
CROT_circ = QuantumCircuit(q, name='CROT')

theta = 2 * pi / (2 ** k)
CROT_circ.cp(theta, 0, 1)
