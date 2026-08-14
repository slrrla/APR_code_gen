from qiskit import QuantumCircuit, execute
from qiskit import Aer

qc = QuantumCircuit(1, 1)
qc.h(0)
qc.measure(0, 0)

backend = Aer.get_backend('qasm_simulator')

# Increase the max_shots limit of the backend's configuration
backend._configuration.max_shots = 2000000

job = execute(qc, backend, shots=1000001)
result = job.result()
print(result.get_counts())
