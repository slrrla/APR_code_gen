# FIX: No transpiler was imported -> import transpile, because Aer requires supported basis instructions.
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
import numpy as np

circ = QuantumCircuit(2, 2)
circ.crx(np.pi/2, 0, 1)
circ.measure_all()

# FIX: Aer received an unsupported crx instruction -> transpile for the backend before running, because this decomposes crx into supported gates.
job = Aer.get_backend('qasm_simulator').run(transpile(circ, Aer.get_backend('qasm_simulator')))
job.result().get_counts()

