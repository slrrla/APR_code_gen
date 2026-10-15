# FIX: Cloud-only Qiskit Runtime Estimator (needs IBM account and remote backend) -> local reference qiskit.primitives Estimator, because it computes the expectation value locally without a service connection
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
from qiskit.primitives import Estimator

qc = QuantumCircuit(1)

O = SparsePauliOp(['Z'])

# FIX: Removed QiskitRuntimeService/Session/Options and remote backend selection -> direct local Estimator run, because the reference primitive needs no session or backend
estimator = Estimator()
job = estimator.run(circuits=[qc], observables=[O])
print(job.result().values)
