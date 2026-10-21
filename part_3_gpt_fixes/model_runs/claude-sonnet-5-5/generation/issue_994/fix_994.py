from qiskit import QuantumCircuit, execute
from qiskit.providers.aer import QasmSimulator

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
# FIX: statevector was never saved in the circuit -> added qc.save_statevector(), because QasmSimulator only stores the state in the result when a save instruction is present
qc.save_statevector()

backend = QasmSimulator()
backend_options = {"method": "statevector"}

job = execute(qc, backend, backend_options=backend_options)
job_result = job.result()
print(job_result.get_statevector(qc))
