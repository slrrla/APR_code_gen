from qiskit import QuantumCircuit, execute
from qiskit import Aer
import numpy as np

def ansatz():
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    return qc

def measure_xx():
    qc = ansatz()
    qc.h(0)
    qc.h(1)
    qc.measure(0, 0)
    qc.measure(1, 1)
    return qc

def measure_yy():
    qc = ansatz()
    qc.rx(-np.pi/2, 0)
    qc.rx(-np.pi/2, 1)
    qc.measure(0, 0)
    qc.measure(1, 1)
    return qc

backend = Aer.get_backend('qasm_simulator')
shots = 8192

def marginal_prob(counts, qubit):
    p0 = 0
    p1 = 0
    for bitstring, c in counts.items():
        bit = bitstring[::-1][qubit]
        if bit == '0':
            p0 += c
        else:
            p1 += c
    return p0 / shots, p1 / shots

qc_xx = measure_xx()
result_xx = execute(qc_xx, backend, shots=shots).result()
counts_xx = result_xx.get_counts()

p0_0, p1_0 = marginal_prob(counts_xx, 0)
p0_1, p1_1 = marginal_prob(counts_xx, 1)

# BUG: treating <X0X1> as the product of the independent single-qubit
# expectation values instead of the joint expectation value.
exp_xx = (p0_0 - p1_0) * (p0_1 - p1_1)

qc_yy = measure_yy()
result_yy = execute(qc_yy, backend, shots=shots).result()
counts_yy = result_yy.get_counts()

p0_0y, p1_0y = marginal_prob(counts_yy, 0)
p0_1y, p1_1y = marginal_prob(counts_yy, 1)

# Same bug applied to <Y0Y1>
exp_yy = (p0_0y - p1_0y) * (p0_1y - p1_1y)

print("<X0X1> =", exp_xx)
print("<Y0Y1> =", exp_yy)
