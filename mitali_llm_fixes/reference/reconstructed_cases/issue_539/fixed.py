# Importing standard Qiskit libraries
from qiskit import QuantumCircuit, transpile
from IPython.display import display
from qiskit.visualization import *
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit_aer import AerSimulator

# Account disabled / API token invalid, so run locally instead of
# authenticating with QiskitRuntimeService against IBM Quantum.
# If you still want to use IBM Quantum, log in on the website,
# copy a fresh API token from the account page and save it with:
# QiskitRuntimeService.save_account(channel="ibm_quantum", token="<NEW_TOKEN>", overwrite=True)

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.measure_all()

backend = AerSimulator()
transpiled = transpile(qc, backend)
result = backend.run(transpiled).result()
counts = result.get_counts()
print(counts)
