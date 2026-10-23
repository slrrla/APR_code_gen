from qiskit import QuantumCircuit, execute, Aer
# FIX: second import from qiskit.providers.ibmq.job shadowed this generic job_monitor -> removed it, because that module needs the separate IBMQ provider and is IBMQ-specific, while the generic monitor works for any backend job
from qiskit.tools.monitor import job_monitor

qc = QuantumCircuit(1, 1)
qc.h(0)
qc.measure(0, 0)

backend = Aer.get_backend('qasm_simulator')
job = execute(qc, backend)

job_monitor(job)

