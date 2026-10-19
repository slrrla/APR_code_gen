from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

backend = AerSimulator()

qc = QuantumCircuit(1)
qc.h(0)
qc.measure_all()

result = backend.run(transpile(qc, backend), shots=1024).result()
print(result.get_counts())
