from qiskit import QuantumCircuit, IBMQ
from qiskit.providers.ibmq.managed import IBMQJobManager

IBMQ.load_account()
provider = IBMQ.get_provider("ibm-q")
backend = provider.get_backend("ibmq_qasm_simulator")

circuits = []
for i in range(3):
    qc = QuantumCircuit(1, 1, name=f"circuit_{i}")
    qc.h(0)
    qc.measure(0, 0)
    circuits.append(qc)

my_shots = 8192

job_manager = IBMQJobManager()
job_set = job_manager.run(circuits, backend=backend, shots=my_shots)
results = job_set.results()
print(results.get_counts(0))
