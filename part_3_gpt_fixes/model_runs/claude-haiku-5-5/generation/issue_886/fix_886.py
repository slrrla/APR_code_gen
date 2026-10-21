# FIX: transpile was not imported -> added it to the qiskit import, because the circuit must be transpiled before running on this backend
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
import numpy as np

circ = QuantumCircuit(2, 2)
circ.crx(np.pi/2, 0, 1)
circ.measure_all()

# FIX: circuit was run untranspiled, so crx was unknown to the backend -> transpile it for the backend before running, because transpilation decomposes crx into supported basis gates
backend = Aer.get_backend('qasm_simulator')
job = backend.run(transpile(circ, backend))
job.result().get_counts()
