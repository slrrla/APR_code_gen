import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, Operator

n = 2  # Size of A
m = 3  # Size of B
k = n + m  # Size of AB

I_AB = np.eye(2**k, 2**k)
I_A = np.eye(2**n, 2**n)

# BUG: attempting to build O'_G by subtracting the identity on B instead of
# the projector onto |0><0| on B. This makes OG trivially zero, which is
# not the intended global observable.
I_B = np.eye(2**m, 2**m)
OG = I_AB - np.kron(I_A, I_B)

# Arbitrary circuit to generate |psi>
qc = QuantumCircuit(k)
qc.h(k - 1)
qc.cx(k - 1, k - 2)
for qb in range(m, 0, -1):
    qc.cx(qb, qb - 1)

# Compute <psi|OG|psi>
sv = Statevector(qc)
OG_op = Operator(OG)
exp_val = sv.expectation_value(OG_op)
print(exp_val)
