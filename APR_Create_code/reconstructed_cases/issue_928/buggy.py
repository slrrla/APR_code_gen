from qiskit import IBMQ

# Load account and get a provider (as the user already had working)
IBMQ.load_account()
provider = IBMQ.get_provider(hub='ibm-q')

job_id = 'job_id_placeholder'

# The user only retrieves the job object itself, expecting it to
# somehow contain gate error / backend configuration information.
retrieve_job = provider.backend.retrieve_job(job_id)

# Just printing the job object does not expose gate errors or
# other backend configuration details.
print(retrieve_job)
