import numpy
from math import pi
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit import Parameter

k = Parameter('k')

q = QuantumRegister(2)
CROT_circ = QuantumCircuit(q, name='CROT')

# FIX: a Qiskit parameter cannot be used as an exponent -> parameterize the angle directly, because nonlinear parameter expressions are unsupported
theta = Parameter('theta')
CROT_circ.cp(theta, 0, 1)
