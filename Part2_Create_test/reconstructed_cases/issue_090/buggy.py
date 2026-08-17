from functools import reduce
from qiskit import QuantumCircuit

# a handful of circuits to compose together
circli = [QuantumCircuit(2) for _ in range(3)]
for qc in circli:
    qc.h(0)
    qc.cx(0, 1)

qcla = QuantumCircuit(2)  # initializer circuit
c = [0, 1]                # single fixed "coordinate" (qubit positions) used every time

# only one iterable (circli) can vary here; c stays the same for every compose call
a = reduce(lambda x, y: x.compose(y, c), circli, qcla)
print(a)
