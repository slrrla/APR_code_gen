# NO BUG: This code uses the Runtime V1 API correctly to run on the selected IBM simulator; it does not configure a fake backend or custom noise model.
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

