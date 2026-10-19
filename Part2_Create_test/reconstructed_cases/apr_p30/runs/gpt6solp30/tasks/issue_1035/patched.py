from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
from qiskit.primitives import BackendEstimator
from qiskit.providers.fake_provider import FakeManila
from qiskit_aer import AerSimulator

# prepare the state |Psi>
qc = QuantumCircuit(1)

# define the operator/observable O
O = SparsePauliOp(['Z'])

# Run locally with the fake device's noise model instead of an IBM Runtime session.
backend = AerSimulator.from_backend(FakeManila())
estimator = BackendEstimator(backend=backend)
job = estimator.run(circuits=[qc], observables=[O])
print(job.result().values)
