from qiskit import QuantumCircuit, execute, Aer
from qiskit.tools.monitor import job_monitor  # only import the one actually needed

qc = QuantumCircuit(1, 1)
qc.h(0)
qc.measure(0, 0)

backend = Aer.get_backend('qasm_simulator')
job = execute(qc, backend)

# qiskit.tools.monitor.job_monitor supports a 'quiet' flag to suppress status messages
job_monitor(job, quiet=True)
