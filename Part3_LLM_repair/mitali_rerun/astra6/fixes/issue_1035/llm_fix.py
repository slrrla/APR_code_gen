from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
# FIX: No fake-device noise model was available -> import FakeManila and NoiseModel, because the Runtime simulator accepts a noise model derived from a fake backend.
from qiskit.providers.fake_provider import FakeManila
from qiskit.providers.aer.noise import NoiseModel
from qiskit_ibm_runtime import QiskitRuntimeService, Options, Session, Estimator

qc = QuantumCircuit(1)

O = SparsePauliOp(['Z'])

service = QiskitRuntimeService()
backend = 'ibmq_qasm_simulator'
# FIX: The simulator had no custom noise configured -> supply FakeManila's noise model, because a fake backend is not itself a remote Runtime backend.
options = Options(resilience_level=0, simulator={"noise_model": NoiseModel.from_backend(FakeManila())})

with Session(service=service, backend=backend) as session:
    estimator = Estimator(session=session, options=options)
    job = estimator.run(circuits=[qc], observables=[O])
    print(job.result().values)
