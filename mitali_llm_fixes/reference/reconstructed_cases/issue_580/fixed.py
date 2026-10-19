from qiskit import Aer

# Backend status must be queried via backend.status(), not job_monitor
backend = Aer.get_backend('qasm_simulator')

print('Status:')
print(' Operational: ', backend.status().operational)
print(' Pending jobs:', backend.status().pending_jobs)
print(' Status message:', backend.status().status_msg)
