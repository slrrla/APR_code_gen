# The user wants to know how to generate a quaternion using Qiskit's
# Quaternion class, and how to use its norm/normalize methods.
# They call the class without the data it requires.
from qiskit.quantum_info.synthesis.quaternion import Quaternion

q = Quaternion()          # missing required quaternion data argument
print(q.norm())
print(q.normalize())
