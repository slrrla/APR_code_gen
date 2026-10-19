from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
from qiskit_ibm_runtime import QiskitRuntimeService, Options, Session, Estimator
# FIX: No fake-backend noise model was available -> import FakeManila and NoiseModel, because Runtime's simulator accepts a noise model derived from a fake backend.
from qiskit.providers.fake_provider import FakeManila
from qiskit_aer.noise import NoiseModel

qc = QuantumCircuit(1)

O = SparsePauliOp(['Z'])

service = QiskitRuntimeService()
backend = 'ibmq_qasm_simulator'
# FIX: The simulator had no fake-backend noise configured -> pass FakeManila's noise model in simulator options, because the Runtime simulator can apply it without using FakeManila as a Runtime backend.
options = Options(resilience_level=0, simulator={"noise_model": NoiseModel.from_backend(FakeManila())})

with Session(service=service, backend=backend) as session:
    estimator = Estimator(session=session, options=options)
    job = estimator.run(circuits=[qc], observables=[O])
    print(job.result().values)
