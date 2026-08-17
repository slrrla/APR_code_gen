import time
from qiskit import IBMQ

IBMQ.load_account()
provider = IBMQ.get_provider(hub='ibm-q')
backend = provider.get_backend('ibmq_qasm_simulator')

inputs = {}
options = {'backend_name': backend.name()}

# Run a runtime job
job = provider.runtime.run(program_id='circuit-runner', inputs=inputs, options=options)

# The job object returned by provider.runtime.run is already the RuntimeJob,
# no need to retrieve it again. If you need to retrieve it later by id, use:
job_id = job.job_id()
job = provider.runtime.job(job_id)

result = job.result()
# The attribute name depends on the program: 'time_taken' for circuit_runner,
# 'optimizer_time' for VQE/QAOA style programs.
time_taken = job.time_taken
print(time_taken)
