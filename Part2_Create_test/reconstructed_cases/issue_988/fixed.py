from qiskit import QuantumCircuit
from qiskit.extensions import YGate

qbit = 0
circ = QuantumCircuit(1)

# Use the .power() method to obtain the principal square root of Y
circ.append(YGate().power(1/2), [qbit])

print(circ)
