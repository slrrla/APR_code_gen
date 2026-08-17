from qiskit_ibm_runtime import QiskitRuntimeService

# Using previously saved account credentials, but the saved token
# is stale/invalid, causing a 401 Unauthorized error when retrieving jobs.
service = QiskitRuntimeService()
job = service.job("JOB_ID")
