from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
from qiskit.primitives import BackendEstimator
from qiskit.providers.fake_provider import FakeManila

# prepare the state |Psi>
qc = QuantumCircuit(1)

# define the operator/observable O
O = SparsePauliOp(['Z'])

# Use a fake backend locally
backend = FakeManila()

# Create BackendEstimator with the fake backend
estimator = BackendEstimator(backend=backend)
job = estimator.run(circuits=[qc], observables=[O])
print(job.result().values)
