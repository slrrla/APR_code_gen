from qiskit_ibm_runtime import QiskitRuntimeService

# Re-save the account with a valid, up-to-date token before using the service.
QiskitRuntimeService.save_account(
    channel='ibm_quantum',
    token='your-token-here',
    overwrite=True
)

service = QiskitRuntimeService()
job = service.job("JOB_ID")
