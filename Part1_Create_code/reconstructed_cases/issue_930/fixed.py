from qiskit import *
from qiskit.extensions import *
import qiskit.extensions.unitary
import cmath as cm
import numpy as np
import math as m
from qiskit.aqua.utils import tensorproduct
from qiskit.aqua.operators import MatrixOp, TensoredOp

n = 10
c = QuantumRegister(1, "c")
q = QuantumRegister(n, "q")
cl = ClassicalRegister(2, "cl")
circ = QuantumCircuit(c, q, cl)

phase = cm.exp(cm.pi * complex(0, 1) * (1 / 4))
matrixR = np.array([[phase, 0], [0, 1]])

_list = []
for _ in range(n):
    _list.append(MatrixOp(matrixR))
tensored_op = TensoredOp(_list)

gateCR = tensored_op.to_circuit().to_gate().control(num_ctrl_qubits=1)
qubits = [m for m in reversed(q)]
circ.append(gateCR, qubits)
