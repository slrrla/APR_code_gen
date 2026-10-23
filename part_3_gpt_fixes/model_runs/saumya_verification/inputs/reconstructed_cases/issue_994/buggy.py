from qiskit import QuantumCircuit, execute
from qiskit.providers.aer import QasmSimulator

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)

backend = QasmSimulator()
backend_options = {"method": "statevector"}

# Circuit execution
job = execute(qc, backend, backend_options=backend_options)
job_result = job.result()
print(job_result.get_statevector(qc))
