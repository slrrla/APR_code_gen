from qiskit import QuantumCircuit, execute
from qiskit import Aer

qc = QuantumCircuit(1, 1)
qc.h(0)
qc.measure(0, 0)

backend = Aer.get_backend('qasm_simulator')

# This exceeds the default max_shots (1000000) of the backend
job = execute(qc, backend, shots=1000001)
result = job.result()
print(result.get_counts())
