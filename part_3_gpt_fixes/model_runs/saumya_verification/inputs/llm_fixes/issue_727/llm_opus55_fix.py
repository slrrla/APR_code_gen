import numpy
from math import pi
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit import Parameter

k = Parameter('k')

q = QuantumRegister(2)
CROT_circ = QuantumCircuit(q, name='CROT')

# FIX: 2 ** k (int raised to a Parameter) is unsupported -> rewrite as numpy.exp(k * numpy.log(2)), because ParameterExpression supports multiplication and exp(), giving the same value 2**k symbolically
theta = 2 * pi / numpy.exp(k * numpy.log(2))
CROT_circ.cp(theta, 0, 1)

