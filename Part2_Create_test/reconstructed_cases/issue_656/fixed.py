from qiskit import IBMQ

IBMQ.load_account()
provider = IBMQ.get_provider('ibm-q')
backend = provider.get_backend('ibmq_16_melbourne')
