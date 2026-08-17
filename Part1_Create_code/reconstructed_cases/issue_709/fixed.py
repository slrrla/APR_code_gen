import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, Operator, SparsePauliOp
from qiskit.primitives.statevector_estimator import StatevectorEstimator

n = 2  # Size of A
m = 3  # Size of B
k = n + m  # Size of AB

I_AB = np.eye(2**k, 2**k)
I_A = np.eye(2**n, 2**n)

# FIX: build the projector onto |0><0| on subsystem B, not the identity.
Zr_B = np.zeros((2**m, 2**m))
Zr_B[0, 0] = 1
OG = I_AB - np.kron(I_A, Zr_B)

# Arbitrary circuit to generate |psi>
qc = QuantumCircuit(k)
qc.h(k - 1)
qc.cx(k - 1, k - 2)
for qb in range(m, 0, -1):
    qc.cx(qb, qb - 1)

# Compute <psi|OG|psi> via Statevector
sv = Statevector(qc)
OG_op = Operator(OG)
exp_val = sv.expectation_value(OG_op)
print(exp_val)

# Compute <psi|OG|psi> via the Estimator primitive
OG_pauli = SparsePauliOp.from_operator(OG_op)
estimator = StatevectorEstimator()
exp_val_estimator = estimator.run([(qc, OG_pauli)]).result()[0].data.evs
print(exp_val_estimator)
