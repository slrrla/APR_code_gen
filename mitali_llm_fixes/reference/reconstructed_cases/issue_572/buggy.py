import numpy as np
from numpy import pi
from qiskit.circuit import QuantumCircuit, Parameter
from qiskit.quantum_info import Operator

theta = Parameter('θ')
qc = QuantumCircuit(2)
qc.cx(0, 1)
qc.crx(theta, 1, 0)  # wrong sign: should be -theta to realize XY(theta)
qc.cx(0, 1)
print(qc)

def XY(theta):
    c = np.cos(theta / 2)
    s = 1j * np.sin(theta / 2)
    return np.array([[1, 0, 0, 0],
                      [0, c, s, 0],
                      [0, s, c, 0],
                      [0, 0, 0, 1]])

val = pi / 14
circ = qc.bind_parameters({theta: val})
print(np.allclose(Operator(circ).data, XY(val)))
