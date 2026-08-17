from qiskit.opflow import X, Z, I, Y

h = (X ^ X ^ I) + (I ^ Y ^ Y) + (Z ^ Z ^ X)

for k in h.to_pauli_op():
    print(k)
