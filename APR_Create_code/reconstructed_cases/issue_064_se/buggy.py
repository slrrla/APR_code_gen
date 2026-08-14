# Minimal reproduction of the reported ImportError.
# Importing qiskit.aqua pulls in scikit-learn, which on this system
# (Ubuntu 14.04, old glibc) fails to load due to a static TLS slot limit.
from qiskit.aqua.operators import PrimitiveOp
