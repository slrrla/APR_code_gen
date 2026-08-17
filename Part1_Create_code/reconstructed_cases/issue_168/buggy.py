import time
from qiskit import IBMQ

IBMQ.load_account()
provider = IBMQ.get_provider(hub='ibm-q')
backend = provider.get_backend('ibmq_qasm_simulator')

inputs = {}
options = {'backend_name': backend.name()}

# Run a runtime job
job = provider.runtime.run(program_id='circuit-runner', inputs=inputs, options=options)

# Incorrectly try to retrieve the same job again using backend.retrieve_job,
# which is meant for regular backend jobs, not runtime jobs
job_id = job.job_id()
job_info = backend.retrieve_job(job_id)

result = job_info.result()
time_taken = job_info.time_taken
print(time_taken)
