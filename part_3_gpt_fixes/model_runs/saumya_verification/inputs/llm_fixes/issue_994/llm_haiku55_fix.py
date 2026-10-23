from qiskit import QuantumCircuit, execute
from qiskit.providers.aer import QasmSimulator

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
# FIX: no statevector was saved by the simulator -> added a save_statevector() instruction at the end of the circuit, because QasmSimulator only returns the statevector when it is explicitly saved
qc.save_statevector()

backend = QasmSimulator()
backend_options = {"method": "statevector"}

job = execute(qc, backend, backend_options=backend_options)
job_result = job.result()
print(job_result.get_statevector(qc))

