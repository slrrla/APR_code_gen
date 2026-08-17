# The 403 error is caused by IBM Quantum blocking requests from the
# user's country/region at the network level (Cloudflare "Access
# denied" page, error 1009). This cannot be fixed from the client
# code - IBMQ.load_account() will keep failing until access from
# that IP/region is no longer blocked (e.g. via VPN or a supported
# network). As a workaround, run circuits locally instead of
# authenticating against IBM Quantum.
from qiskit import Aer

backend = Aer.get_backend('qasm_simulator')
