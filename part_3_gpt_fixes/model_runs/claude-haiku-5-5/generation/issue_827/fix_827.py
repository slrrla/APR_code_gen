from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
# FIX: imported deprecated 'compile' -> import 'transpile' and 'assemble' instead, because compile() is deprecated and the warning asks to use these two functions
from qiskit import Aer, transpile, assemble
from qiskit.backends.jobstatus import JOB_FINAL_STATES

n_qubits = 5
qc_list = []
for i in range(n_qubits):
    qr = QuantumRegister(n_qubits)
    cr = ClassicalRegister(n_qubits)
    qc = QuantumCircuit(qr, cr)
    qc.x(qr[i])
    qc.measure(qr, cr)
    qc_list.append(qc)

backend = Aer.get_backend('qasm_simulator')

# FIX: used deprecated compile(qc, backend) -> transpile the circuit for the backend, then assemble it into a qobj, because compile() is deprecated and removed
qobj_list = [assemble(transpile(qc, backend)) for qc in qc_list]
job_list = [backend.run(qobj) for qobj in qobj_list]

while job_list:
    for job in job_list:
        if job.status() in JOB_FINAL_STATES:
            job_list.remove(job)
            print(job.result().get_counts())
