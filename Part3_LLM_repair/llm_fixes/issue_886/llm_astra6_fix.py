from qiskit import QuantumCircuit
from qiskit_aer import Aer
import numpy as np

circ = QuantumCircuit(2, 2)
circ.crx(np.pi/2, 0, 1)
circ.measure_all()

# FIX: Aer does not directly support crx -> decompose the circuit before execution, because crx decomposes into supported gates.
job = Aer.get_backend('qasm_simulator').run(circ.decompose())
job.result().get_counts()

