import numpy as np
from qiskit.quantum_info import Statevector, SparsePauliOp

O = SparsePauliOp(data=["II", "IZ", "ZI", "ZZ", "XX"], coeffs=[-1, 0.4, -0.4, -1, 0.1])

psi = np.sqrt(1/2) * (Statevector.from_label('00') + Statevector.from_label('11'))

# trying to compute <psi|O^2|psi> but forgot to square the operator
exp_val = psi.expectation_value(O)
print(exp_val)
