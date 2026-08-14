# Use qiskit-ibm-runtime's QiskitRuntimeService to fetch historical
# calibration data for a specific backend and date.
from qiskit_ibm_runtime import QiskitRuntimeService
from datetime import datetime

service = QiskitRuntimeService()
ibmq_manila = service.backend('ibmq_manila')

when = datetime(day=15, month=4, year=2023)  # April 15th, 2023
properties_20230415 = ibmq_manila.properties(datetime=when)
print(properties_20230415.last_update_date)
