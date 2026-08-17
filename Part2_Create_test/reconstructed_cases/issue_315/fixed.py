from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

qc_combine = QuantumCircuit(2)
qc_combine.h(0)
qc_combine.cx(0, 1)
qc_combine.measure_all()

shots_used = 1024

backend = AerSimulator(method='statevector')

# How to define the number of processors that are used by simulator?
backend.set_options(
    max_parallel_threads=0,        # Use all CPU cores
    max_parallel_experiments=0,
    max_parallel_shots=42,
    statevector_parallel_threshold=16
)

job = backend.run(qc_combine, shots=shots_used)
result = job.result()
counts = result.get_counts(qc_combine)
print(counts)
