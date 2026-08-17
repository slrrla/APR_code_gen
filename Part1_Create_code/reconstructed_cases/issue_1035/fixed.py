from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
from qiskit.primitives import BackendEstimator
from qiskit.providers.fake_provider import FakeNairobi

# prepare the state |Psi>
qc = QuantumCircuit(1)

# define the operator/observable O
O = SparsePauliOp(['Z'])

# Use a local fake backend instead of Qiskit Runtime service/session,
# via the generic BackendEstimator primitive which works with any backend.
estimator = BackendEstimator(backend=FakeNairobi())
job = estimator.run(qc, O)
result = job.result()
print(result.values)
