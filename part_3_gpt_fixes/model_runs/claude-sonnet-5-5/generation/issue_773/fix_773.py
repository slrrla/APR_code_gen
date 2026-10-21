from qiskit import QuantumCircuit, execute, Aer
from qiskit.tools.monitor import job_monitor
# FIX: duplicate import of job_monitor from the ibmq provider shadowed the generic one -> removed it, because the generic qiskit.tools.monitor job_monitor works for any backend and the ibmq package is deprecated/not needed for Aer jobs

qc = QuantumCircuit(1, 1)
qc.h(0)
qc.measure(0, 0)

backend = Aer.get_backend('qasm_simulator')
job = execute(qc, backend)

job_monitor(job)
