import numpy as np
from qiskit.quantum_info.synthesis.quaternion import Quaternion

# Generate a random quaternion (4 real components) and use the
# Quaternion class methods as intended.
data = np.random.rand(4)
q = Quaternion(data)

print(q.norm())
q = q.normalize()
print(q.norm())
