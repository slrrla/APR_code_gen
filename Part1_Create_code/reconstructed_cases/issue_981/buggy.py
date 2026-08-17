import numpy as np
from qiskit.chemistry import FermionicOperator

# Naive attempt: build a uniform nearest-neighbor hopping matrix,
# without properly indexing the alternating (dimerized) coupling t_ij.
n = 10
h1 = np.zeros((n, n), dtype=np.complex_)
for i in range(n - 1):
    h1[i, i + 1] = 1
    h1[i + 1, i] = 1

fer_op = FermionicOperator(h1=h1)
