from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit_aer import AerSimulator

# Pulls the latest calibration data every time it is run,
# so the resulting simulator is not reproducible over time.
service = QiskitRuntimeService(channel="ibm_quantum", token="MY_TOKEN")
backend = service.backend("ibm_brisbane")
simulator = AerSimulator.from_backend(backend)
