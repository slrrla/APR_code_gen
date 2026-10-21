from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
from qiskit_ibm_runtime import QiskitRuntimeService, Options, Session, Estimator
from qiskit_aer.noise import NoiseModel
from qiskit.providers.fake_provider import FakeManila

qc = QuantumCircuit(1)

O = SparsePauliOp(['Z'])

service = QiskitRuntimeService()
backend = 'ibmq_qasm_simulator'
# FIX: options ran the cloud simulator noiselessly, with no fake backend noise -> pass a noise model built from FakeManila via the simulator option, because the Runtime simulator accepts a custom noise model this way
options = Options(resilience_level=0, simulator={"noise_model": NoiseModel.from_backend(FakeManila())})

with Session(service=service, backend=backend) as session:
    estimator = Estimator(session=session, options=options)
    job = estimator.run(circuits=[qc], observables=[O])
    print(job.result().values)
