from qiskit import QuantumCircuit, execute
from qiskit.providers.aer import QasmSimulator

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
# FIX: no state was saved by the simulator, so get_statevector had nothing to return -> added qc.save_statevector(), because the statevector method only stores the state when a save instruction is present
qc.save_statevector()

backend = QasmSimulator()
backend_options = {"method": "statevector"}

job = execute(qc, backend, backend_options=backend_options)
job_result = job.result()
print(job_result.get_statevector(qc))
