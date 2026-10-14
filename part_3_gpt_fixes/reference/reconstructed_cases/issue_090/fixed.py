from functools import reduce
from qiskit import QuantumCircuit

circli = [QuantumCircuit(2) for _ in range(3)]
for qc in circli:
    qc.h(0)
    qc.cx(0, 1)

qcla = QuantumCircuit(2)  # initializer circuit
c = [0, 1]                # example coordinate
cs = [c] * len(circli)    # one coordinate per circuit (could differ per entry)

# zip the two iterables together and carry both the composed circuit and a running
# sum of the "x coordinates" of c through the accumulator tuple
a, x_sum = reduce(
    lambda x, y: (x[0].compose(y[0], y[1]), [x[1][0] + y[1][0]]),
    zip(circli, cs),
    (qcla, [0]),
)
print(a)
print(x_sum)
