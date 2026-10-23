# FIX: crx is unsupported as a native Aer instruction -> import transpile, because the circuit must be compiled to the backend's supported basis gates
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
import numpy as np

circ = QuantumCircuit(2, 2)
circ.crx(np.pi/2, 0, 1)
circ.measure_all()

# FIX: the untranspiled crx instruction caused AerError -> transpile the circuit for qasm_simulator, because Aer only accepts supported basis instructions
job = Aer.get_backend('qasm_simulator').run(transpile(circ, Aer.get_backend('qasm_simulator')))
job.result().get_counts()

