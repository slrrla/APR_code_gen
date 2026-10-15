from qiskit import QuantumCircuit, execute, Aer
# FIX: duplicate job_monitor import from qiskit.providers.ibmq.job shadowed this one -> removed the second import, because the generic qiskit.tools.monitor.job_monitor works for any backend job, including Aer, and the ibmq one is IBMQ-specific
from qiskit.tools.monitor import job_monitor

qc = QuantumCircuit(1, 1)
qc.h(0)
qc.measure(0, 0)

backend = Aer.get_backend('qasm_simulator')
job = execute(qc, backend)

job_monitor(job)
