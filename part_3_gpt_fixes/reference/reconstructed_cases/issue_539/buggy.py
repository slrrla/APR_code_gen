# Importing standard Qiskit libraries
from qiskit import QuantumCircuit, transpile
from IPython.display import display
from qiskit.visualization import *
from qiskit_ibm_runtime import QiskitRuntimeService

# Loading your IBM Quantum account(s)
service = QiskitRuntimeService(channel="ibm_quantum")  # the error occurs here!
# qiskit_ibm_runtime.api.exceptions.RequestsApiError: '403 Client Error: Forbidden for url:
# https://auth.quantum-computing.ibm.com/api/users/loginWithToken. Your IBM Quantum
# account has been disabled. Learn more: https://ibm.biz/BdfaME., Error code: 3485.'

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.measure_all()

transpiled = transpile(qc, service.backend("ibmq_qasm_simulator"))
