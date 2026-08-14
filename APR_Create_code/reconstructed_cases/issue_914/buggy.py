from qiskit import QuantumCircuit, Aer, QuantumRegister, ClassicalRegister
import qiskit
from qiskit import IBMQ
import numpy as np
from qiskit.circuit.library import QFT
from math import pi

def set_input_state(a, b):
    get_binary = lambda x: '{0:{fill}3b}'.format(x, fill='0')
    r_a = QuantumRegister(3, 'a')
    r_b = QuantumRegister(3, 'b')
    cr = ClassicalRegister(3, 'c')
    qc = QuantumCircuit(r_a, r_b, cr)
    a_binary = get_binary(a)
    b_binary = get_binary(b)
    for i in range(3):
        if a_binary[i] == '1':
            qc.x(r_a[2 - i])
        if b_binary[i] == '1':
            qc.x(r_b[2 - i])
    return qc, r_a, r_b, cr

def controlled_rotations(qc, reg_a, reg_b, n):
    for i in range(0, n + 1):
        qc.cp(np.pi / 2**i, reg_b[n - i], reg_a[n])

a = 1
b = 3
qc, r_a, r_b, cr = set_input_state(a, b)
# BUG: QFT applied without swaps, missing the necessary SWAP layer
qc.append(QFT(3, do_swaps=False), [2, 1, 0])
for i in range(0, 3):
    controlled_rotations(qc, r_a, r_b, 2 - i)
qc.append(QFT(3, do_swaps=False).inverse(), [2, 1, 0])
qc.measure(r_a, cr)
qc.draw('mpl')

backend = Aer.get_backend('qasm_simulator')
job = qiskit.execute(qc, backend, shots=100)
result = job.result()
counts = result.get_counts(qc)
print(counts)
