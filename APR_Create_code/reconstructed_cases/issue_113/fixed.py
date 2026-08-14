import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import StatePreparation

L = [2, 1, 2, 0, 0, 1, 3, 2]

len_qr1 = int(np.ceil(np.log2(len(L))))
len_qr2 = int(np.log2(max(L))) + 1
num_qubits = len_qr1 + len_qr2

statevector = np.zeros(2**num_qubits)
for i, el in enumerate(L):
    index_reg = '{0:b}'.format(i).zfill(len_qr1)
    element_reg = '{0:b}'.format(el).zfill(len_qr2)
    statevector[int(element_reg + index_reg, 2)] = 1

statevector /= np.linalg.norm(statevector)

qc = QuantumCircuit(num_qubits)
sp = StatePreparation(statevector)
qc.append(sp, range(num_qubits))
