from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
from qiskit.primitives import BackendEstimator
from qiskit.providers.fake_provider import FakeManila

# prepare the state |Psi>
qc = QuantumCircuit(1)

# define the operator/observable O
O = SparsePauliOp(['Z'])

# Run locally with FakeManila's noise model (via Qiskit Aer).
# Noise and finite shots can shift the estimate away from the ideal value 1.
backend = FakeManila()
estimator = BackendEstimator(backend=backend, options={'shots': 4096})
job = estimator.run(circuits=[qc], observables=[O])
print(job.result().values)
