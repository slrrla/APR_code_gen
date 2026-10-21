import numpy
from math import pi
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit import Parameter

k = Parameter('k')

q = QuantumRegister(2)
CROT_circ = QuantumCircuit(q, name='CROT')

# FIX: 2 ** k is unsupported for a Parameter (no __rpow__) -> rewrote 1/2**k as exp(-k*ln2) using numpy, because it only needs multiplication and exp of the parameter expression
theta = 2 * pi * numpy.exp(-k * numpy.log(2))
CROT_circ.cp(theta, 0, 1)
