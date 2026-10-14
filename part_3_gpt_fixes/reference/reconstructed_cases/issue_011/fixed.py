import math

import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import QFT, UnitaryGate

N = 21
a = 4
work_qubits = math.ceil(math.log2(N))
control_qubits = 2 * math.ceil(math.log2(N))


def controlled_modular_multiplication(multiplier, modulus, n_qubits):
    dim = 2 ** n_qubits
    matrix = np.zeros((2 * dim, 2 * dim))
    for x in range(dim):
        matrix[x, x] = 1.0
        target = (multiplier * x) % modulus if x < modulus else x
        matrix[dim + target, dim + x] = 1.0
    return UnitaryGate(matrix, label=f"c-x{multiplier}mod{modulus}")


qc = QuantumCircuit(control_qubits + work_qubits, control_qubits)
qc.h(range(control_qubits))
qc.x(control_qubits)

work = list(range(control_qubits, control_qubits + work_qubits))
for k in range(control_qubits):
    qc.append(controlled_modular_multiplication(pow(a, 2 ** k, N), N, work_qubits), work + [k])

qc.append(QFT(control_qubits, inverse=True), range(control_qubits))
qc.measure(range(control_qubits), range(control_qubits))

print(N, control_qubits, work_qubits, qc.num_qubits)
