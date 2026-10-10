from qiskit import QuantumCircuit, execute, Aer
from qiskit.tools.monitor import job_monitor
# FIX: The IBMQ-specific import overwrote the general monitor -> removed it, because this job runs on Aer.

qc = QuantumCircuit(1, 1)
qc.h(0)
qc.measure(0, 0)

backend = Aer.get_backend('qasm_simulator')
job = execute(qc, backend)

job_monitor(job)

