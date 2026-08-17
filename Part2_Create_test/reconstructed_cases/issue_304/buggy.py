from qiskit.opflow import X, Y, Z

op = 2*(X^X) + 0.5*(Z^Y)

# Trying to directly get the inverse observable - no such method exists
inv_op = op.inverse()
print(inv_op)
