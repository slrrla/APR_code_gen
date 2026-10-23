# FIX: Live-provider access cannot supply a retired system -> import FakeOslo, because it contains an archived ibm_oslo calibration snapshot, not necessarily the experiment's calibration.
from qiskit.providers.fake_provider import FakeOslo

# FIX: Retired ibm_oslo is unavailable through get_backend -> use its archived snapshot, because its properties remain accessible without contacting the retired system.
backend = FakeOslo()

system = backend
print(system.properties().backend_version)
print(system.properties().last_update_date)
print(system.properties().qubits)

