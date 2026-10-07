from qiskit import QuantumCircuit
from qiskit.providers.basic_provider import BasicProvider

qc_combine = QuantumCircuit(2)
qc_combine.h(0)
qc_combine.cx(0, 1)
qc_combine.measure_all()

shots_used = 1024

backend = BasicProvider().get_backend("basic_simulator")

# Note: In Qiskit 2.5.0, BasicProvider backend supports different options.
# The following options are no longer available: max_parallel_threads,
# max_parallel_experiments, max_parallel_shots, statevector_parallel_threshold

job = backend.run(qc_combine, shots=shots_used)
result = job.result()
counts = result.get_counts(qc_combine)
print(counts)
