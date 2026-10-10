from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
# FIX: Runtime's Estimator requires an IBM Runtime backend -> use Aer, because fake backends run locally.
from qiskit_aer.primitives import Estimator
from qiskit_aer.noise import NoiseModel
from qiskit.providers.fake_provider import FakeManila

qc = QuantumCircuit(1)

O = SparsePauliOp(['Z'])

# FIX: A Runtime backend name cannot select a local fake backend -> build a noise model from FakeManila, because Aer can simulate it locally.
backend = FakeManila()
noise_model = NoiseModel.from_backend(backend)

# FIX: Runtime sessions cannot run fake backends -> configure Aer Estimator with the fake backend's noise model.
estimator = Estimator(backend_options={"noise_model": noise_model})
job = estimator.run(circuits=[qc], observables=[O])
print(job.result().values)
