from qiskit import QuantumCircuit, Aer
from qiskit.providers.ibmq.managed import IBMQJobManager

# Minimal circuit used for the batch of jobs
qc = QuantumCircuit(1, 1)
qc.h(0)
qc.measure(0, 0)

# Simulate a batch of 375 circuits (as in the reported scenario)
item = [qc] * 375

backend = Aer.get_backend('qasm_simulator')
job_manager = IBMQJobManager()

# NOTE: With qiskit < 0.23.2, a transient network error during submission
# can cause the same job to be submitted twice (a "phantom" duplicate job).
job_set = job_manager.run(item, backend=backend, name='L_5_vqe_qc', shots=8192)
