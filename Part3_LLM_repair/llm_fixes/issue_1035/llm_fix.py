from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
# FIX: Qiskit Runtime primitives require IBM Quantum backends -> use Aer Estimator with a fake-backend noise model, because fake backends cannot be used with Runtime sessions
from qiskit_aer.noise import NoiseModel
from qiskit_aer.primitives import Estimator
from qiskit.providers.fake_provider import FakeManila

qc = QuantumCircuit(1)

O = SparsePauliOp(['Z'])

# FIX: Runtime service and session cannot accept fake backends -> construct a local estimator with FakeManila's noise model, because Aer supports simulated backend noise
backend = FakeManila()
estimator = Estimator(backend_options={'noise_model': NoiseModel.from_backend(backend)})
job = estimator.run(circuits=[qc], observables=[O])
print(job.result().values)

