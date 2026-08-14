from qiskit_ibm_runtime import QiskitRuntimeService

# Save an IBM Cloud account on disk
token = '***'  # <== Use your token here
QiskitRuntimeService.save_account(channel="ibm_quantum", token=token, overwrite=True)

# Read default credentials from disk
service = QiskitRuntimeService()
