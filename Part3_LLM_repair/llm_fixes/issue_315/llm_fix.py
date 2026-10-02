from qiskit import QuantumCircuit
from qiskit.providers.basic_provider import BasicProvider

qc_combine = QuantumCircuit(2)
qc_combine.h(0)
qc_combine.cx(0, 1)
qc_combine.measure_all()

shots_used = 1024

backend = BasicProvider().get_backend("basic_simulator")

# FIX: Removed unsupported parallelization options -> use the BasicSimulator defaults, because these fields are not valid for this backend
job = backend.run(qc_combine, shots=shots_used)
result = job.result()
counts = result.get_counts(qc_combine)
print(counts)

