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

def joint_expectation(counts):
    # Correct: X0X1 (or Y0Y1) is an operator on the joint state, with
    # eigenvalue +1 on |00>,|11> and -1 on |01>,|10>.
    total = sum(counts.values())
    exp = 0
    for bitstring, c in counts.items():
        bits = bitstring[::-1]
        b0 = int(bits[0])
        b1 = int(bits[1])
        sign = 1 if b0 == b1 else -1
        exp += sign * c
    return exp / total

qc_xx = measure_xx()
result_xx = execute(qc_xx, backend, shots=shots).result()
counts_xx = result_xx.get_counts()

exp_xx = joint_expectation(counts_xx)

qc_yy = measure_yy()
result_yy = execute(qc_yy, backend, shots=shots).result()
counts_yy = result_yy.get_counts()

exp_yy = joint_expectation(counts_yy)

print("<X0X1> =", exp_xx)
print("<Y0Y1> =", exp_yy)
