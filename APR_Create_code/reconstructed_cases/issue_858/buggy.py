from qiskit import IBMQ

# Attempt to access a retired backend's properties directly.
# This fails because retired backends can no longer be reached
# through the provider.
provider = IBMQ.load_account()
backend = provider.get_backend('ibm_oslo')

system = backend
print(system.properties().backend_version)
print(system.properties().last_update_date)
print(system.properties().qubits)
