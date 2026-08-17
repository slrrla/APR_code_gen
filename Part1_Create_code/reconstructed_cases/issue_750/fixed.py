import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator, Pauli

# Build the equivalent operator via a circuit, applying Z on qubit 0 and X on qubit 2
qc = QuantumCircuit(3)
qc.z(0)
qc.x(2)
op = Operator(qc)
print(op)

# Alternative ways to construct the same operator using tensor/expand
X = Operator(Pauli('X'))
Z = Operator(Pauli('Z'))
I = Operator(Pauli('I'))

IZ = I.tensor(Z)
result_a = X.tensor(IZ)

XI = X.tensor(I)
result_b = XI.tensor(Z)

ZI = Z.expand(I)
result_c = ZI.expand(X)

print(result_a)
print(result_b)
print(result_c)
