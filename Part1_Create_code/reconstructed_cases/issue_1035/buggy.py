from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
from qiskit_ibm_runtime import QiskitRuntimeService, Options, Session, Estimator

# prepare the state |Psi>
qc = QuantumCircuit(1)

# define the operator/observable O
O = SparsePauliOp(['Z'])

# This requires a real IBM Quantum account/network connection,
# and only runs on a real (or cloud) simulator backend, not a local fake backend.
service = QiskitRuntimeService()
backend = 'ibmq_qasm_simulator'
options = Options(resilience_level=0)

with Session(service=service, backend=backend) as session:
    estimator = Estimator(session=session, options=options)
    job = estimator.run(circuits=[qc], observables=[O])
    print(job.result().values)
