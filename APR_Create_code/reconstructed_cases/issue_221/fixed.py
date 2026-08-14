from qiskit import QuantumCircuit
from pprint import pprint

circ = QuantumCircuit(2)
circ.h(0)
circ.cx(0, 1)

# read the elements of the circuit via its data attribute
print(circ.data)
pprint(vars(circ.data))
