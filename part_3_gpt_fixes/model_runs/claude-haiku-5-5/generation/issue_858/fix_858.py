# NO BUG: The code correctly requests properties from a backend via the provider API, but 'ibm_oslo' is retired and no longer exposed by get_backend, so the failure is due to the backend's retirement rather than a code error.
from qiskit import IBMQ

provider = IBMQ.load_account()
backend = provider.get_backend('ibm_oslo')

system = backend
print(system.properties().backend_version)
print(system.properties().last_update_date)
print(system.properties().qubits)
