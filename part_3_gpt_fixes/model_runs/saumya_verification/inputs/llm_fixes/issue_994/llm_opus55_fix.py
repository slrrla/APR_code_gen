from qiskit import QuantumCircuit, execute
from qiskit.providers.aer import QasmSimulator

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
# FIX: QasmSimulator does not store the statevector unless asked -> added qc.save_statevector(), because the save instruction puts the final statevector into the result data
qc.save_statevector()

backend = QasmSimulator()
backend_options = {"method": "statevector"}

# FIX: backend_options= keyword is deprecated/removed in execute -> unpacked the options as run kwargs, because execute forwards extra kwargs to backend.run as simulator options
job = execute(qc, backend, **backend_options)
job_result = job.result()
print(job_result.get_statevector(qc))
