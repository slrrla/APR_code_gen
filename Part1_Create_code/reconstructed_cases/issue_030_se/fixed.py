import numpy as np
from functools import reduce
from qiskit import QuantumCircuit

# build a list of 10 small circuits paired with the qubits to compose onto
circ_list = []
for _ in range(10):
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.crz(np.pi/2, 0, 1)
    circ_list.append((qc, [2, 3]))  # [2,3] is a random choice

qcl = QuantumCircuit(8, 8)

qcom = reduce(lambda x, y: x.compose(y[0], y[1]), circ_list, qcl)

print(qcom)
