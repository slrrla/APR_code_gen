import numpy as np
from qiskit import QuantumCircuit

# build a list of 10 small circuits
circ_list = []
for _ in range(10):
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.crz(np.pi/2, 0, 1)
    circ_list.append(qc)

qcl = QuantumCircuit(8, 8)

# manually repeating compose for each small circuit - not accumulated properly
for i in range(len(circ_list)):
    qcom = qcl.compose(circ_list[i], [2, 3])  # [2,3] is a random choice

print(qcom)
