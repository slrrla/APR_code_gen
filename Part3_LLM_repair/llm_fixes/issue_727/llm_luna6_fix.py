import numpy
from math import pi
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit import Parameter

k = Parameter('k')

q = QuantumRegister(2)
CROT_circ = QuantumCircuit(q, name='CROT')

# FIX: integer exponentiation cannot use a symbolic Parameter -> express the reciprocal power with exp, because Qiskit supports that symbolic expression
theta = 2 * pi * numpy.exp(-k * numpy.log(2))
CROT_circ.cp(theta, 0, 1)

