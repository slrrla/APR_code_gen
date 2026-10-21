from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
import numpy as np

circ = QuantumCircuit(2, 2)
circ.crx(np.pi/2, 0, 1)
circ.measure_all()

backend = Aer.get_backend('qasm_simulator')
# FIX: circuit was run without transpiling -> transpile the circuit for the backend before running, because Aer then receives only gates it supports instead of the unknown 'crx' instruction
job = backend.run(transpile(circ, backend))
job.result().get_counts()
