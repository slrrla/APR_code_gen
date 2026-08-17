from qiskit import QuantumCircuit
from qiskit_aer import Aer
import numpy as np
from qiskit import transpile

circ = QuantumCircuit(2)
circ.crx(np.pi/2, 0, 1)
circ.measure_all()

backend = Aer.get_backend('qasm_simulator')

# Transpiling your circuit
transpile_circ = transpile(circ, backend=backend)

job = backend.run(transpile_circ, shots=1024)
job.result().get_counts()
