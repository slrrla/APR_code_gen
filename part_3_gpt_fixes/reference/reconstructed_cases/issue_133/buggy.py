# Minimal reproduction of the reported import errors with modern qiskit (1.x)
from qiskit.visualization import (
    array_to_latex,
    plot_bloch_vector,
    plot_bloch_multivector,
    plot_state_qsphere,
    plot_state_city,
)
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, transpile
from qiskit import execute, Aer  # execute/Aer no longer exist in qiskit>=1.0
import qiskit.quantum_info as qi
from qiskit.quantum_info import SparsePauliOp
from qiskit.extensions import Initialize  # qiskit.extensions removed in qiskit>=1.0

import numpy as np
import matplotlib.pyplot as plt

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.measure_all()

backend = Aer.get_backend('aer_simulator')
result = execute(qc, backend, shots=1024).result()
print(result.get_counts())
