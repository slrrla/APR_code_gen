from qiskit import IBMQ

IBMQ.load_account()
backend = IBMQ.get_backend('ibmq_16_melbourne', 'ibm-q')
