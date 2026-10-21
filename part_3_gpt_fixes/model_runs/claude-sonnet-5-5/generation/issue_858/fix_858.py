from qiskit_ibm_runtime import QiskitRuntimeService

# FIX: IBMQ provider was removed from Qiskit -> use QiskitRuntimeService, because it is the current way to load an account and get backends
service = QiskitRuntimeService()
backend = service.backend('ibm_oslo')

system = backend
print(system.backend_version)
# FIX: BackendV2 has no properties() -> use target.qubit_properties, because it holds per-qubit T1/T2 data
print(system.target.qubit_properties)
