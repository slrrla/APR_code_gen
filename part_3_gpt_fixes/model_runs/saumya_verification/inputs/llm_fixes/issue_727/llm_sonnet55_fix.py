import numpy
from math import pi
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit import Parameter

k = Parameter('k')

q = QuantumRegister(2)
CROT_circ = QuantumCircuit(q, name='CROT')

# FIX: `2 ** k` raises TypeError because Parameter has no __rpow__ -> rewrote 2**k as (k * ln 2).exp(), because 2**k == exp(k*ln2) and ParameterExpression supports exp()
theta = 2 * pi / ((k * numpy.log(2)).exp())
CROT_circ.cp(theta, 0, 1)
