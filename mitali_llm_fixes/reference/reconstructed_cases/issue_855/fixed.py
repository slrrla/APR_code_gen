import time
import numpy as np
from qiskit.circuit.gate import Gate
from qiskit.quantum_info.synthesis import two_qubit_cnot_decompose

Dmatrix = np.array([[-1/3, 2/3, 0, 2/3],
                     [ 2/3, -1/3, 0, 2/3],
                     [ 0, 0, -1, 0],
                     [ 2/3, 2/3, 0, -1/3]])

decomp = two_qubit_cnot_decompose(Dmatrix)

class CustomDGate(Gate):
    def __init__(self, label=None):
        super().__init__("dgate", 2, [], label=label)

    def _define(self):
        self.definition = decomp.copy()

    def __array__(self, dtype=None):
        return np.asarray(Dmatrix, dtype=dtype)

Dgate = CustomDGate()

st = time.time()
C6Dgate = Dgate.control(6)
print(round(time.time() - st, 2))
