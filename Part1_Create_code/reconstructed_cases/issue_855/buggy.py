import time
import numpy as np
from qiskit.extensions import UnitaryGate

Dmatrix = np.array([[-1/3, 2/3, 0, 2/3],
                     [ 2/3, -1/3, 0, 2/3],
                     [ 0, 0, -1, 0],
                     [ 2/3, 2/3, 0, -1/3]])

Dgate = UnitaryGate(Dmatrix)

st = time.time()
C6Dgate = Dgate.control(6)  # Step that takes a long time
print(round(time.time() - st, 2))  # print ~70 secs
