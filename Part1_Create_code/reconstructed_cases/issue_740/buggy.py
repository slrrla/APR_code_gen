from qiskit_ibm_provider import IBMProvider

provider = IBMProvider(instance="ibm-q/open/main")
backend = provider.get_backend('ibmq_lima')
# The error: QiskitBackendNotFoundError: 'No backend matches the criteria'
