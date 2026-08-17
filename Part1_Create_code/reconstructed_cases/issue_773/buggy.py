from qiskit import QuantumCircuit, execute, Aer
from qiskit.tools.monitor import job_monitor
from qiskit.providers.ibmq.job import job_monitor  # duplicate import shadows the first one

qc = QuantumCircuit(1, 1)
qc.h(0)
qc.measure(0, 0)

backend = Aer.get_backend('qasm_simulator')
job = execute(qc, backend)

# unclear which job_monitor is actually being used here
job_monitor(job)
