from qiskit.quantum_info import SparsePauliOp
from qiskit.circuit import Parameter

# Build a parameterized SparsePauliOp representing exp(-i(XZ*a + YZ*b))
a, b = Parameter('a'), Parameter('b')
op = SparsePauliOp(['XZ', 'YZ'], coeffs=[a, b])

# Old opflow-style approach: try to exponentiate directly with exp_i()
# This fails because SparsePauliOp has no exp_i() method (that was an
# opflow PauliOp/Pauli method, now deprecated/removed).
evolved = op.exp_i()

print(evolved)
