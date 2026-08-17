from qiskit import QuantumCircuit, Aer
from qiskit.providers.ibmq.managed import IBMQJobManager
import qiskit

# The duplicate-submission bug was fixed in qiskit 0.23.2, which cancels
# phantom jobs earlier so they no longer consume the job limit.
assert qiskit.__version__ >= '0.23.2', "Upgrade qiskit to >=0.23.2 to avoid duplicate job submissions"

# Minimal circuit used for the batch of jobs
qc = QuantumCircuit(1, 1)
qc.h(0)
qc.measure(0, 0)

# Simulate a batch of 375 circuits (as in the reported scenario)
item = [qc] * 375

backend = Aer.get_backend('qasm_simulator')
job_manager = IBMQJobManager()

job_set = job_manager.run(item, backend=backend, name='L_5_vqe_qc', shots=8192)
