# Attempt to fetch historical calibration data using the old, now-removed
# IBMQ provider API (this is the approach referenced in the linked
# "archive of calibration data" threads that the asker says always errors).
from qiskit import IBMQ
from datetime import datetime

IBMQ.load_account()
provider = IBMQ.get_provider(hub='ibm-q')
backend = provider.get_backend('ibmq_manila')

when = datetime(day=15, month=4, year=2023)  # April 15th, 2023
properties_20230415 = backend.properties(datetime=when)
print(properties_20230415.last_update_date)
