from qiskit_ibm_runtime import QiskitRuntimeService

service = QiskitRuntimeService()
job_id = 'abcde'
job = service.job(job_id)

# Retrieve the executed circuits from the job's stored inputs.
pubs = job.inputs['pubs']
circuits = [pub[0] for pub in pubs]
print(circuits)
