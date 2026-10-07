from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
from qiskit.providers.fake_provider import FakeManila
from qiskit.primitives import BackendEstimator as Estimator

# prepare the state |Psi>
qc = QuantumCircuit(1)

# define the operator/observable O
O = SparsePauliOp(['Z'])

# BackendEstimator wraps the fake device's local simulator, including noise.
backend = FakeManila()
options = {"shots": 8192, "seed_simulator": 123}
estimator = Estimator(backend=backend, options=options)
job = estimator.run(circuits=[qc], observables=[O])
print(job.result().values)
