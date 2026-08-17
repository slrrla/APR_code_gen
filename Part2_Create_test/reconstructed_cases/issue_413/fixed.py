import qiskit
print(qiskit.__qiskit_version__)  # check that qiskit-ibmq-provider >= 0.8, which added combine_results

from qiskit import QuantumCircuit, Aer
from qiskit.providers.ibmq.managed import IBMQJobManager

# Local simulator standing in for the real ibmq_backend (no network calls)
backend = Aer.get_backend('qasm_simulator')

circs = [QuantumCircuit(2, 2) for _ in range(2)]
for qc in circs:
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])

job_set = IBMQJobManager().run(circs, backend=backend, name='job-set-abc')
job_results = job_set.results()
job_results_combined = job_results.combine_results()
job_counts_combined = job_results_combined.get_counts()
