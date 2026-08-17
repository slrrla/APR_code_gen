# Measurement error mitigation using qiskit-ibm-runtime primitives with resilience_level
from qiskit import QuantumCircuit
from qiskit_ibm_runtime import QiskitRuntimeService, Estimator
from qiskit.quantum_info import SparsePauliOp

# Use a local/simulated runtime service, no real backend contact
service = QiskitRuntimeService(channel="local")

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)

observable = SparsePauliOp("ZZ")

# resilience_level enables built-in error mitigation
estimator = Estimator(session=service, options={"resilience_level": 1})

job = estimator.run(circuits=[qc], observables=[observable])
result = job.result()
print(result.values)
