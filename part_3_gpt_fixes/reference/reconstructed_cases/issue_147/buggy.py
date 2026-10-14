# Minimize 5*x1 - 7*x2 binary x1 x2
# QISKit
#
# The user has a binary optimization problem but does not know how to
# express or solve it using Qiskit. No solver is actually run here.

from qiskit.optimization import QuadraticProgram

# construct optimization problem
qp = QuadraticProgram()
qp.binary_var('x1')
qp.binary_var('x2')
qp.minimize(linear=[5, -7])

# problem is defined but never solved
print(qp)
