# FIX: legacy IBMQ provider (removed) cannot reach retired ibm_oslo -> import FakeOslo snapshot, because it stores the device's recorded calibration properties
from qiskit_ibm_runtime.fake_provider import FakeOslo

# FIX: provider.get_backend('ibm_oslo') on a retired device -> instantiate FakeOslo(), because it exposes the archived properties offline
backend = FakeOslo()

system = backend
print(system.properties().backend_version)
print(system.properties().last_update_date)
print(system.properties().qubits)
