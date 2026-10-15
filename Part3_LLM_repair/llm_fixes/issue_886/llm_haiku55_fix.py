# FIX: transpile was not imported -> added it to the qiskit import, because the circuit must be transpiled to be used below
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
import numpy as np

circ = QuantumCircuit(2, 2)
circ.crx(np.pi/2, 0, 1)
circ.measure_all()

# FIX: circuit was run untranspiled, so the unsupported crx gate reached Aer -> transpile it for the backend before running, because Aer only accepts its basis gates
job = Aer.get_backend('qasm_simulator').run(transpile(circ, Aer.get_backend('qasm_simulator')))
job.result().get_counts()
