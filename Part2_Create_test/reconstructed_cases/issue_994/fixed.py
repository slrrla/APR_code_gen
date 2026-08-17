from qiskit import QuantumCircuit, execute
from qiskit.providers.aer import QasmSimulator
from qiskit.providers.aer.extensions import snapshot_statevector  # registers qc.snapshot

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.snapshot('final', snapshot_type='statevector')

backend = QasmSimulator()
backend_options = {"method": "statevector"}

# Circuit execution
job = execute(qc, backend, backend_options=backend_options)
job_result = job.result()

# get_statevector will not work on QasmSimulator results;
# the statevector is stored as a snapshot instead
statevector = job_result.data(qc)['snapshots']['statevector']['final'][0]
print(statevector)
