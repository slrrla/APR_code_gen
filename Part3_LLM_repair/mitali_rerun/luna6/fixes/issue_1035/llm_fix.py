# FIX: Runtime Estimator requires an IBM Quantum service backend -> use Aer and a fake backend, because fake-backend noise is simulated locally
from qiskit_aer.primitives import Estimator
from qiskit.providers.fake_provider import FakeManila
from qiskit_aer.noise import NoiseModel

from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp

qc = QuantumCircuit(1)

O = SparsePauliOp(['Z'])

# FIX: a Runtime Session cannot run on a local fake backend -> build an Aer Estimator with its noise model, because Aer runs locally
backend = FakeManila()
noise_model = NoiseModel.from_backend(backend)
estimator = Estimator(backend_options={"noise_model": noise_model})
job = estimator.run(circuits=[qc], observables=[O])
print(job.result().values)
