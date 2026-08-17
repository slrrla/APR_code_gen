from qiskit import QuantumCircuit, execute, Aer

# Build many small circuits to submit as a single job.
circuits = []
for i in range(5):
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])
    circuits.append(qc)

backend = Aer.get_backend('qasm_simulator')

# qiskit.execute submits everything as one job.
# It does NOT split circuits across multiple jobs if the backend's
# per-job limit is exceeded, so this can fail for large batches.
job = execute(circuits, backend, shots=1024)
result = job.result()
print(result.get_counts())
