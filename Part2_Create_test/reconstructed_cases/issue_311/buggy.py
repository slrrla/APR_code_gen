from qiskit import QuantumCircuit, execute, Aer
from qiskit.tools.monitor import job_monitor

# Local simulator standing in for the ibmq_manhattan hardware backend
backend = Aer.get_backend('qasm_simulator')

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.measure_all()

# Attempting to submit a very large batch of circuits (reported as 3200)
all_qc = [qc for _ in range(3200)]

# Single execute() call with a huge circuit list and shots, which
# on the real hardware backend caused the job to be cancelled
job = execute(all_qc, backend=backend, shots=8096)
job_monitor(job)
