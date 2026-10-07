from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
from qiskit.primitives import BackendEstimator
from qiskit.providers.fake_provider import FakeManila

# prepare the state |Psi>
qc = QuantumCircuit(1)

# define the operator/observable O
O = SparsePauliOp(['Z'])

# Run the primitive locally on a fake backend instead of Qiskit Runtime
backend = FakeManila()
estimator = BackendEstimator(backend=backend)
job = estimator.run(circuits=[qc], observables=[O])
print(job.result().values)
