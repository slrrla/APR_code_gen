from qiskit import QuantumCircuit, execute, IBMQ

# Load account and pick a backend (real device or IBMQ simulator)
provider = IBMQ.load_account()
backend = provider.get_backend('ibmq_qasm_simulator')

qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])

job = execute(qc, backend=backend, shots=1024, optimization_level=0)

# Save the job id so we can retrieve the job later, even after
# restarting the kernel or losing the original 'job' variable
job_id = job.job_id()
print(job_id)

# ... time passes, kernel restarted, 'job' variable no longer exists
# Retrieve the job from the backend using the saved job_id
job = backend.retrieve_job(job_id)
result = job.result()
print(result.get_counts())
