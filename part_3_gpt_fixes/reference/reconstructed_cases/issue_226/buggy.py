from qiskit import QuantumCircuit
from qiskit.opflow import Z, CircuitOp

N = 3
i, j, k = 0, 1, 2

# Author's original approach requires building circuits every time
circZZ = QuantumCircuit(N)  # circuit for Z_i Z_j
circZ = QuantumCircuit(N)   # circuit for Z_k
circZZ.z(i)
circZZ.z(j)
circZ.z(k)

opZZ = CircuitOp(circZZ)  # convert circuit to operator
opZ = CircuitOp(circZ)    # convert circuit to operator

op = opZZ + opZ

print(op)
