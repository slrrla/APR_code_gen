# FIX: IBMQ cannot retrieve a retired backend -> import FakeOslo, because it contains an archived snapshot of ibm_oslo's properties.
from qiskit.providers.fake_provider import FakeOslo

# FIX: Live account lookup cannot reach ibm_oslo -> instantiate FakeOslo, because its archived properties are available locally.
backend = FakeOslo()

system = backend
print(system.properties().backend_version)
print(system.properties().last_update_date)
print(system.properties().qubits)
