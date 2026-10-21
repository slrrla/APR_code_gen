from qiskit import QuantumCircuit, execute, Aer
# FIX: duplicate `job_monitor` import from qiskit.providers.ibmq.job shadowed the generic one and expects an IBMQJob, not an Aer job -> removed the shadowing import so the generic qiskit.tools.monitor.job_monitor is used, because it works with any job type
from qiskit.tools.monitor import job_monitor

qc = QuantumCircuit(1, 1)
qc.h(0)
qc.measure(0, 0)

backend = Aer.get_backend('qasm_simulator')
job = execute(qc, backend)

job_monitor(job)
