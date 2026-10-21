import numpy
from math import pi
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit import Parameter

k = Parameter('k')

q = QuantumRegister(2)
CROT_circ = QuantumCircuit(q, name='CROT')

# FIX: 2 ** k raises TypeError (int ** Parameter unsupported) -> rewrite 2**k as exp(k*ln2), because ParameterExpression supports multiplication and .exp()
theta = 2 * pi / (k * numpy.log(2)).exp()
CROT_circ.cp(theta, 0, 1)
