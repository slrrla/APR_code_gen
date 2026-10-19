from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
from qiskit.primitives import Estimator

# prepare the state |Psi>
qc = QuantumCircuit(1)

# define the operator/observable O
O = SparsePauliOp(['Z'])

# Use Qiskit's local Estimator primitive; Runtime sessions require the
# separate qiskit-ibm-runtime package and a cloud service.
estimator = Estimator()
job = estimator.run(circuits=[qc], observables=[O])
print(job.result().values)
