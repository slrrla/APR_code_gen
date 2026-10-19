from qiskit import QuantumCircuit
from qiskit.extensions import YGate

qbit = 0
circ = QuantumCircuit(1)

# Attempt to get the principal square root of the Pauli Y gate
# by using the ** operator directly on the gate object.
circ.append(YGate() ** (1/2), [qbit])

print(circ)
