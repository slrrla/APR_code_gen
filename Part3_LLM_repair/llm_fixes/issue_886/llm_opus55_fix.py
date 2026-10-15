# FIX: transpile was not imported -> added it to the qiskit import, because the circuit must be transpiled before running
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
import numpy as np

circ = QuantumCircuit(2, 2)
circ.crx(np.pi/2, 0, 1)
circ.measure_all()

# FIX: circuit with crx was sent to the backend untranspiled -> transpile it for the backend first, because the simulator does not support crx natively and needs it decomposed into its basis gates
job = Aer.get_backend('qasm_simulator').run(transpile(circ, Aer.get_backend('qasm_simulator')))
job.result().get_counts()
