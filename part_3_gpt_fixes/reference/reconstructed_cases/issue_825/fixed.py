from numpy import pi
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
from qiskit.circuit.library import RYGate

theta = Parameter('theta')
CCCRY = RYGate(theta).control(3)

circuit = QuantumCircuit(4)
circuit.append(CCCRY, [0, 1, 2, 3])
circuit.draw('mpl')
