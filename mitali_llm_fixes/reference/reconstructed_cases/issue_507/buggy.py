# Reported bug: IBMQ.load_account() raises "403 Client Error: Forbidden"
# when trying to reach IBM Quantum's authentication servers.
from qiskit import IBMQ

# This call fails with a 403 Client Error because IBM Quantum's
# Cloudflare-protected auth endpoint rejects the request (the error
# body reveals it is a region/IP based access ban, not a credentials
# problem).
IBMQ.load_account()

provider = IBMQ.get_provider()
backend = provider.get_backend('ibmq_qasm_simulator')
