from qiskit import QuantumCircuit, execute, Aer
from qiskit.tools.monitor import job_monitor

# Author believed job_monitor could be used to check backend status
backend = Aer.get_backend('qasm_simulator')

qc = QuantumCircuit(1, 1)
qc.h(0)
qc.measure(0, 0)

job = execute(qc, backend)
job_monitor(job)
