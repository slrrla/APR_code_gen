from qiskit import QuantumCircuit, execute, Aer
# FIX: The IBMQ-specific import shadowed the generic monitor -> keep only the generic import, because the job runs on Aer rather than IBMQ.
from qiskit.tools.monitor import job_monitor

qc = QuantumCircuit(1, 1)
qc.h(0)
qc.measure(0, 0)

backend = Aer.get_backend('qasm_simulator')
job = execute(qc, backend)

job_monitor(job)

