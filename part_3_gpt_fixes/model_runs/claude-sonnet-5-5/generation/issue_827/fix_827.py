from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
# FIX: removed `compile` import and added transpile/assemble -> import transpile and assemble, because qiskit.compile was removed
from qiskit import Aer, transpile, assemble
# FIX: old module path qiskit.backends no longer exists -> use qiskit.providers.jobstatus, because the module was renamed
from qiskit.providers.jobstatus import JOB_FINAL_STATES

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

# FIX: deprecated/removed compile() -> use assemble(transpile(...)), because that is the replacement producing a runnable qobj
qobj_list = [assemble(transpile(qc, backend)) for qc in qc_list]
job_list = [backend.run(qobj) for qobj in qobj_list]

while job_list:
    for job in job_list:
        if job.status() in JOB_FINAL_STATES:
            job_list.remove(job)
            print(job.result().get_counts())
