from qiskit import IBMQ

provider = IBMQ.load_account()
backend = provider.get_backend('ibm_oslo')

system = backend
print(system.properties().backend_version)
print(system.properties().last_update_date)
print(system.properties().qubits)
