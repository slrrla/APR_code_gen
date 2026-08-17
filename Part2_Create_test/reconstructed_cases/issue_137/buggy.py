from qiskit import QuantumCircuit, IBMQ, execute

# Build a simple circuit
qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])

# Load IBMQ account and get a real backend
IBMQ.load_account()
provider = IBMQ.get_provider(hub='ibm-q')
backend = provider.get_backend('ibmq_athens')

# Submitting the job repeatedly fails with:
# IBMQBackendApiError: 'Error submitting job: ...
# HTTPSConnectionPool(host='s3.us-east.cloud-object-storage.appdomain.cloud', port=443):
# Max retries exceeded with url: ... (Caused by SSLError(SysCallError(60, 'ETIMEDOUT')))
job = execute(qc, backend=backend, shots=1024)
result = job.result()
print(result.get_counts(qc))
