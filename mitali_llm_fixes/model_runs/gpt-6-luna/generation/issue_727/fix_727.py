import numpy
from math import pi
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit import Parameter

k = Parameter('k')

q = QuantumRegister(2)
CROT_circ = QuantumCircuit(q, name='CROT')

# FIX: int ** Parameter is unsupported -> use an exponential expression, because it represents the same parameterized power.
theta = 2 * pi / numpy.exp(k * numpy.log(2))
CROT_circ.cp(theta, 0, 1)
