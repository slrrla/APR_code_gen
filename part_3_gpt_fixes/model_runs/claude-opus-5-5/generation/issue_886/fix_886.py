# FIX: transpile was not imported -> added transpile to the qiskit import, because it is needed to decompose crx for the backend
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
import numpy as np

circ = QuantumCircuit(2, 2)
circ.crx(np.pi/2, 0, 1)
circ.measure_all()

# FIX: circuit was run untranspiled so Aer rejected the crx instruction -> transpile circ for the backend before run, because transpiling rewrites crx into the backend's supported basis gates
backend = Aer.get_backend('qasm_simulator')
job = backend.run(transpile(circ, backend))
job.result().get_counts()
