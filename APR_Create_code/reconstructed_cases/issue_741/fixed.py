from qiskit import QuantumCircuit, transpile
from qiskit.providers.aer import AerSimulator

qc = QuantumCircuit(3)
qc.h(0)
qc.cx(0, 1)
qc.cx(1, 2)

backend = AerSimulator()

# At optimization_level=3, qiskit's transpile() defaults to using DenseLayout
transpiled_qc = transpile(qc, backend=backend, optimization_level=3, layout_method='dense')
print(transpiled_qc)
