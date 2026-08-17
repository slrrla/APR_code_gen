from qiskit import QuantumCircuit
from qiskit_aer import Aer
import numpy as np

circ = QuantumCircuit(2, 2)
circ.crx(np.pi/2, 0, 1)
circ.measure_all()

job = Aer.get_backend('qasm_simulator').run(circ)
job.result().get_counts()
