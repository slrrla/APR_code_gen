import numpy
from math import pi
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit import Parameter

k = Parameter('k')

q = QuantumRegister(2)
CROT_circ = QuantumCircuit(q, name='CROT')

# FIX: int ** Parameter is unsupported -> rewrote 2**k as exp(k*ln(2)) using ParameterExpression.exp(), because it is mathematically equal and supported symbolically
theta = 2 * pi / (k * numpy.log(2)).exp()
CROT_circ.cp(theta, 0, 1)
