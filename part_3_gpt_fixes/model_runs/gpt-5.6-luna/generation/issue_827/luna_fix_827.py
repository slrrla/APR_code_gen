from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
# FIX: deprecated compile import -> use transpile and assemble from qiskit.compiler, because compile() is deprecated
from qiskit import Aer
from qiskit.compiler import transpile, assemble
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

# FIX: deprecated compile() -> transpile circuits and assemble the runnable Qobjs, because compile() is deprecated
qobj_list = [assemble(transpile(qc, backend), backend) for qc in qc_list]
job_list = [backend.run(qobj) for qobj in qobj_list]

while job_list:
    for job in job_list:
        if job.status() in JOB_FINAL_STATES:
            job_list.remove(job)
            print(job.result().get_counts())
