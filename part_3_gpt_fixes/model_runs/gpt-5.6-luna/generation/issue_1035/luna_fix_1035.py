# FIX: Runtime service sessions cannot execute on fake backends -> use the runtime primitive's local mode, because fake backends are not IBM Quantum service backends
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
from qiskit_ibm_runtime import Options, Estimator
from qiskit_ibm_runtime.fake_provider import FakeManila

qc = QuantumCircuit(1)

O = SparsePauliOp(['Z'])

# FIX: a fake backend cannot be selected by name through QiskitRuntimeService -> instantiate it locally, because fake backends run outside the IBM Quantum service
backend = FakeManila()
options = Options(resilience_level=0)

# FIX: Session submits jobs to the IBM Quantum service -> construct the estimator in local mode, because this executes against the fake backend locally
estimator = Estimator(mode=backend, options=options)
job = estimator.run(circuits=[qc], observables=[O])
print(job.result().values)
