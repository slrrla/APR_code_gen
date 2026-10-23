# NO BUG: This code correctly uses the Runtime Estimator API shown with a cloud simulator; adding fake-backend noise would be an enhancement rather than a bug fix.
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
from qiskit_ibm_runtime import QiskitRuntimeService, Options, Session, Estimator

qc = QuantumCircuit(1)

O = SparsePauliOp(['Z'])

service = QiskitRuntimeService()
backend = 'ibmq_qasm_simulator'
options = Options(resilience_level=0)

with Session(service=service, backend=backend) as session:
    estimator = Estimator(session=session, options=options)
    job = estimator.run(circuits=[qc], observables=[O])
    print(job.result().values)

