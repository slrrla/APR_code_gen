# FIX: legacy IBMQ provider (removed) and retired 'ibm_oslo' cannot be reached -> import the FakeOslo snapshot backend, because it ships the recorded ibm_oslo calibration properties offline
from qiskit_ibm_runtime.fake_provider import FakeOslo

# FIX: provider.get_backend('ibm_oslo') on a retired device fails -> instantiate FakeOslo(), because its properties() returns the stored ibm_oslo data
backend = FakeOslo()

system = backend
print(system.properties().backend_version)
print(system.properties().last_update_date)
print(system.properties().qubits)

