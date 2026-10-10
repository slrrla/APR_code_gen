import numpy
from math import pi
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit import Parameter

k = Parameter('k')

q = QuantumRegister(2)
CROT_circ = QuantumCircuit(q, name='CROT')

# FIX: Raising 2 to a Parameter is unsupported -> use exp(k * log(2)), because it represents the same power using supported parameter operations.
theta = 2 * pi / (k * numpy.log(2)).exp()
CROT_circ.cp(theta, 0, 1)

