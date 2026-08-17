from qiskit import QuantumCircuit, transpile, Aer
from qiskit.compiler import assemble
from qiskit.providers.ibmq.managed import IBMQJobManager

# Build many small circuits to submit as a single job.
circuits = []
for i in range(5):
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])
    circuits.append(qc)

backend = Aer.get_backend('qasm_simulator')

# qiskit.execute internally does transpile() + assemble() + backend.run(),
# but IBMQJobManager.run also does transpile() + assemble() and additionally
# splits circuits into multiple jobs (and consolidates results) if the
# number of circuits exceeds the backend's per-job limit.
transpiled = transpile(circuits, backend)

job_manager = IBMQJobManager()
job_set = job_manager.run(transpiled, backend=backend, shots=1024)
result = job_set.results()
print(result.get_counts(0))
