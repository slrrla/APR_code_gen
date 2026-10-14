from qiskit import IBMQ

provider = IBMQ.load_account()
# FIX: retired backends are excluded by default -> request a non-operational backend, because ibm_oslo is no longer active
backend = provider.get_backend('ibm_oslo', operational=False)

system = backend
print(system.properties().backend_version)
print(system.properties().last_update_date)
print(system.properties().qubits)
