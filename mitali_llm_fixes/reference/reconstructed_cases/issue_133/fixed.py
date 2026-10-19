# Fixed: drop the removed 'execute' and 'Initialize' imports, use qiskit_aer for Aer
from qiskit.visualization import (
    array_to_latex,
    plot_bloch_vector,
    plot_bloch_multivector,
    plot_state_qsphere,
    plot_state_city,
)
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, transpile
from qiskit_aer import Aer  # Aer now lives in the separate qiskit-aer package
import qiskit.quantum_info as qi
from qiskit.quantum_info import SparsePauliOp

import numpy as np
import matplotlib.pyplot as plt

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.measure_all()

backend = Aer.get_backend('aer_simulator')
transpiled = transpile(qc, backend)
result = backend.run(transpiled, shots=1024).result()
print(result.get_counts())
