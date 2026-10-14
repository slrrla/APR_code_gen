from qiskit import *
from qiskit.extensions import *
import qiskit.extensions.unitary
import cmath as cm
import numpy as np
import math as m
from qiskit.aqua.utils import tensorproduct

n = 10
c = QuantumRegister(1, "c")
q = QuantumRegister(n, "q")
cl = ClassicalRegister(2, "cl")
circ = QuantumCircuit(c, q, cl)

phase = cm.exp(cm.pi * complex(0, 1) * (1 / 4))
matrixR = np.array([[phase, 0], [0, 1]])
matrixTe = matrixR
for _ in range(n - 1):
    matrixTe = tensorproduct(matrixTe, matrixR)
matrixOp = matrixTe

gateCR = UnitaryGate(matrixOp).control(num_ctrl_qubits=1)
qubits = [m for m in reversed(q)]
circ.append(gateCR, qubits)
