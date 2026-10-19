from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit import Aer
from qiskit.compiler import transpile, assemble
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
transpiled_circs = transpile(qc_list, backend=backend)
qobj = assemble(transpiled_circs, backend=backend)
job = backend.run(qobj)

while not job.status() in JOB_FINAL_STATES:
    pass
print(job.result().get_counts())
