import numpy as np
from qiskit.quantum_info import Statevector, SparsePauliOp

O = SparsePauliOp(data=["II", "IZ", "ZI", "ZZ", "XX"], coeffs=[-1, 0.4, -0.4, -1, 0.1])

O_sqr = O @ O

psi = np.sqrt(1/2) * (Statevector.from_label('00') + Statevector.from_label('11'))

exp_val = psi.expectation_value(O_sqr)
print(exp_val)
