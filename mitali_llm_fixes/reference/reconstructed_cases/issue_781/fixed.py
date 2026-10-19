from qiskit import QuantumCircuit, qpy
from qiskit.circuit import Parameter

theta = Parameter("$\\Theta$")
qc = QuantumCircuit(1)
qc.ry(theta, 0)

with open("qc.qpy", "wb") as qpy_file_write:
    qpy.dump(qc, qpy_file_write)

import numpy as np

with open("qc.qpy", "rb") as qpy_file_read:
    qc_loaded = qpy.load(qpy_file_read)[0]

qc_loaded = qc_loaded.bind_parameters([np.pi / 2])
qc_loaded.draw("mpl")
