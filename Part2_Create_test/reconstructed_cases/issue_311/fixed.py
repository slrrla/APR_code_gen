from qiskit import QuantumCircuit, Aer
from qiskit.providers.ibmq.managed import IBMQJobManager

# Local simulator standing in for the ibmq_manhattan hardware backend
backend = Aer.get_backend('qasm_simulator')

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.measure_all()

# Same large batch of circuits (reported as 3200)
all_qc = [qc for _ in range(3200)]

# IBMQJobManager splits the circuit list into multiple jobs that respect
# the backend's max_experiments/max_shots limits, and collects the results
job_manager = IBMQJobManager()
job_set = job_manager.run(all_qc, backend=backend, shots=8096)
results = job_set.results()
