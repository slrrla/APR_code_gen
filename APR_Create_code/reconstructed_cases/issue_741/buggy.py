from qiskit import QuantumCircuit, transpile
from qiskit.providers.aer import AerSimulator

qc = QuantumCircuit(3)
qc.h(0)
qc.cx(0, 1)
qc.cx(1, 2)

backend = AerSimulator()

# It's unclear which layout method is used by default when optimization_level=3
transpiled_qc = transpile(qc, backend=backend, optimization_level=3)
print(transpiled_qc)
