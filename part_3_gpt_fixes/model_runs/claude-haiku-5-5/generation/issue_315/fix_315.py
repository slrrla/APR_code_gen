from qiskit import QuantumCircuit
from qiskit.providers.basic_provider import BasicProvider

qc_combine = QuantumCircuit(2)
qc_combine.h(0)
qc_combine.cx(0, 1)
qc_combine.measure_all()

shots_used = 1024

backend = BasicProvider().get_backend("basic_simulator")

# FIX: set_options used Aer-only fields (max_parallel_threads, etc.) that BasicProvider's basic_simulator does not accept -> removed the set_options call, because the basic simulator runs without these settings and the fields are only valid for qiskit-aer's backends
job = backend.run(qc_combine, shots=shots_used)
result = job.result()
counts = result.get_counts(qc_combine)
print(counts)
