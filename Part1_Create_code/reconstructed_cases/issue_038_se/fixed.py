# Fixed: use qiskit-ibmq-provider (the qiskit.providers.ibmq module) instead
# of the deprecated IBMQuantumExperience library.
from qiskit import IBMQ

API_TOKEN = 'MY_API_TOKEN'

IBMQ.save_account(API_TOKEN, overwrite=True)
IBMQ.load_account()

provider = IBMQ.get_provider()

# Note: the credit system has been removed from the new IBM Q Experience,
# so there is no API call to check remaining credits anymore.
print(provider.backends())
