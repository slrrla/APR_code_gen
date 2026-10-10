from qiskit import IBMQ

provider = IBMQ.load_account()
# FIX: `ibm_oslo` is not the backend's name -> use `ibmq_oslo`, because the retired system was published under that name
backend = provider.get_backend('ibmq_oslo')

system = backend
print(system.properties().backend_version)
print(system.properties().last_update_date)
print(system.properties().qubits)

